import datetime
from datetime import timedelta
from itertools import product
import urllib

from lxml import etree
from repoze.bfg.renderers import render

import config

_cache = {}

def getOutboundDates(search):
    """ Given a search, return all possible outbound dates for the
        date range of the search.

    """
    today = datetime.date.today()
    if today>search['end_date']:
        return []
    start_date = max([search['start_date'], today])

    dates = []
    for dow in search['departdaysofweek']:
        date = start_date
        if date.isoweekday()!=dow:
            date = date + \
                   timedelta((dow - date.isoweekday()) % 7)

        while date<search['end_date'] and date<today+timedelta(days=config.FUTURE_DISTANCE):
            dates.append(date)
            date = date + timedelta(7)

    return dates

def getReturnDates(outbound_date, num_days, end_date):
    today = datetime.date.today()
    return_dates = []
    for period in num_days:
        next_date = outbound_date + timedelta(period)
        if next_date<end_date and next_date<today+timedelta(days=config.FUTURE_DISTANCE):
            return_dates.append(next_date)
    return return_dates

def getSearchCombos(search):
    """ Given a search dict, generate a list of combinations of
        outbound and return journey options.

    """
    combinations = []
    outbound_dates = getOutboundDates(search)

    outbound_options = product(outbound_dates,
                               search['origins'],
                               search['destinations'])
    for outbound_option in outbound_options:
        return_options = [x for x in product(getReturnDates(outbound_option[0], search['num_days'], search['end_date']),
                                 (outbound_option[2],),
                                 (outbound_option[1],))]
        if return_options:
            combinations.append((outbound_option, return_options))

    return combinations

def performSearch(root, search):
    availability = []
    for outbound_option, return_options in getSearchCombos(search):
        journies = []
        for return_option in return_options:
            j = getAvailability(root, outbound_option[0], return_option[0], outbound_option[1], outbound_option[2], **search)
            journies.extend(j)

        if not journies:
            continue
        # sort by price
        price_sorter = lambda x,y: cmp(x['price'],y['price'])
        journies.sort(price_sorter)
        if journies[0]['price'] > search['price']:
            continue

        # find out how many options are below our price threshold
        journies = filter(lambda x: x['price']<search['price'], journies)
        for journey in journies:
            journey = {
                       'origin': outbound_option[1],
                       'destination': outbound_option[2],
                       'outbound_depart': journey['outbound_details'][0],
                       'outbound_arrive': journey['outbound_details'][1],
                       'outbound_changes': journey['outbound_details'][2],
                       'return_depart': journey['return_details'][0],
                       'return_arrive': journey['return_details'][1],
                       'return_changes': journey['return_details'][2],
                       'book_link': journey['booking_link'],
                       'total_price': journey['price']
                     }
            availability.append(journey)

    return availability

def getAvailability(root, outbound_date, return_date, origin, dest, adults=0, children=0, infants=0, **kwargs):
    """ @param date.date
        @param str
        @param str
        @param str
        @param int
        @param int
        @param int
        @return a list of journeys matching the criteria. Journeys are
                in the form of a dict of departure datetime, arrival
                datetime, num changes, price, booking link

    """

    availability_cache = root.availability_cache
    if config.USE_CACHE:
        if (outbound_date, return_date, origin, dest, adults, children, infants) in availability_cache and \
           (datetime.datetime.now()-availability_cache[(outbound_date, return_date, origin, dest, adults, children, infants)][1])<datetime.timedelta(hours=config.EXPIRE_CACHE):
            return availability_cache[(outbound_date, return_date, origin, dest, adults, children, infants)][0]

    request = config.GetAvailabilityRequest % \
                     {'guid': config.GUID,
                      'origin': origin,
                      'dest': dest,
                      'outbound_date': outbound_date.strftime('%d/%m/%Y'),
                      'return_date': return_date.strftime('%d/%m/%Y'),
                      'num_adults': adults,
                      'num_children': children,
                      'num_infants': infants}
    request = urllib.urlencode({'requestMessage': request})
    request_url = '%s/GetAvailability' % (config.API_URL,)
    try:
        response = urllib.urlopen(request_url, request).read()
    except:
        # TODO: be more specific
        return []
    try:
        response = etree.fromstring(response).text
        response = etree.fromstring(response)
    except:
        # TODO: be more specific
        return []
    # TODO: check for success tag
    journeys = []
    for journey in response.xpath('//PricedItinerary'):
        (outbound_option, return_option) = journey.xpath('AirItinerary/OriginDestinationOptions/OriginDestinationOption')
        outbound_details = getDetails(outbound_option)
        return_details = getDetails(return_option)
        price = float(journey.xpath('AirItineraryPricingInfo/ItinTotalFare/TotalFare/@Amount')[0])
        booking_link = journey.xpath('BmiBookingLink/text()')[0].strip()
        journeys.append({
                         'outbound_details': outbound_details,
                         'return_details': return_details,
                         'price': price,
                         'booking_link': booking_link
                         })

    if config.USE_CACHE:
        root.availability_cache[(outbound_date, return_date, origin, dest, adults, children, infants)]=(journeys, datetime.datetime.now())

    return journeys

def getDetails(option):
    departure_datetime = option.xpath('FlightSegment[1]/@DepartureDateTime')[0]
    departure_datetime = datetime.datetime.strptime(departure_datetime,
                                           '%m/%d/%Y %H:%M:%S')
    arrival_datetime = option.xpath('FlightSegment[last()]/@ArrivalDateTime')[0]
    arrival_datetime = datetime.datetime.strptime(arrival_datetime,
                                         '%m/%d/%Y %H:%M:%S')
    num_changes = int(option.xpath('count(FlightSegment)'))-1
    return (departure_datetime, arrival_datetime, num_changes)