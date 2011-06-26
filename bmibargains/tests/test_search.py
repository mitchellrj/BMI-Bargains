# -*- coding: utf8 -*-

import datetime
import unittest

import mock
from bmibargains import search

example_search = {
          'departdaysofweek': [1,2,3,4,5,6,7],
          'origins': ['MAN','LDS'],
          'destinations': ['ALC', 'PRA'],
          'price': 60,
          'num_days': [3,4,5],
          'start_date': datetime.date.today(),
          'end_date': datetime.date.today(),
          'adults': 1,
          'children': 0,
          'infants': 0,
         }

class TestGetAvailability(unittest.TestCase):
    def setUp(self):
        self.getAvailability = search.getAvailability
        self.render = search.render
        search.render = lambda x,y: str(y)
        self.urllib = search.urllib
        search.urllib = mock.Mock()
        search.urllib.urlopen.return_value = \
"""<?xml version="1.0" encoding="UTF-8"?>
<ARC_OTA_AirLowFareSearchRS TimeStamp="10/07/2008 13:34:27"> <Success />
<PricedItineraries LowestPricedItinerary="1" LowestFareAmount="132.00" LowestFareCurrency="GBP"> <PricedItinerary SequenceNumber="1">
<BmiBookingLink><![CDATA[ http://www.flybmi.com/book/book.aspx?reqtyp=AIR&officeID=EMABD08ZZ&language=GB&market=UK&country=GB&ibeSource=ARC:BmiArcDevAccount&cityfrominput0=LHR&citytoinput0=MAN&oneway=1&day0=1&month0=9&fb_numpaxADT=2&fb_numpaxCHD=1&fb_numpaxINF=0]]></BmiBookingLink> <AirItinerary>
<OriginDestinationOptions> <OriginDestinationOption FareType="EconomySaver">
<FlightSegment DepartureDateTime="01/09/2008 06:55:00" ArrivalDateTime="01/09/2008 08:00:00">
<DepartureAirport LocationCode="LHR" Terminal="1" /> <ArrivalAirport LocationCode="MAN" Terminal="3" /> <OperatingAirline FlightNumber="582" CompanyShortName="BMI" /> <Equipment AirEquipType="Airbus Industrie A319" />
</FlightSegment> </OriginDestinationOption>
</OriginDestinationOptions> </AirItinerary>
<AirItineraryPricingInfo> <ItinTotalFare>
<BaseFare Amount="12.00" CurrencyCode="GBP" /> <Taxes>
<Tax TaxCode="ALL" Amount="120.00" CurrencyCode="GBP" /> </Taxes>
<TotalFare Amount="132.00" CurrencyCode="GBP" /> </ItinTotalFare>
</AirItineraryPricingInfo> </PricedItinerary>
<PricedItinerary SequenceNumber="2">
<BmiBookingLink><![CDATA[ http://www.flybmi.com/book/book.aspx?reqtyp=AIR&officeID=EMABD08ZZ&language=GB&market=UK&country=GB&ibeSource=ARC:BmiArcDevAccount&cityfrominput0=LHR&citytoinput0=MAN&oneway=1&day0=1&month0=9&fb_numpaxADT=2&fb_numpaxCHD=1&fb_numpaxINF=0]]></BmiBookingLink>
<AirItinerary> <OriginDestinationOptions>
<OriginDestinationOption FareType="EconomyFlexible"> <FlightSegment DepartureDateTime="01/09/2008 19:20:00" ArrivalDateTime="01/09/2008 20:25:00">
<DepartureAirport LocationCode="LHR" Terminal="1" /> <ArrivalAirport LocationCode="MAN" Terminal="3" /> <OperatingAirline FlightNumber="592" CompanyShortName="BMI" /> <Equipment AirEquipType="Airbus Industrie A319" />
</FlightSegment> </OriginDestinationOption>
</OriginDestinationOptions> </AirItinerary>
<AirItineraryPricingInfo> <ItinTotalFare>
<BaseFare Amount="387.00" CurrencyCode="GBP" /> <Taxes>
<Tax TaxCode="ALL" Amount="120.00" CurrencyCode="GBP" /> </Taxes>
<TotalFare Amount="507.00" CurrencyCode="GBP" /> </ItinTotalFare>
</AirItineraryPricingInfo> </PricedItinerary>
<!--
This example has been trucated, the complete response contains 23 <PricedItenerary> elements representing all bookable journeys found.
-->
</PricedItineraries> </ARC_OTA_AirLowFareSearchRS>"""

    def tearDown(self):
        search.urllib = self.urllib
        search.render = self.render

    def test_getAvailabilityXPaths(self):
        result = self.getAvailability(datetime.date.today(), 'ORIGIN', 'DEST')
        self.assertEqual(len(result), 2)
        for r in result:
            self.assertEqual(r['num_changes'], 0)
            self.assertTrue(r['booking_link'] in ('http://www.flybmi.com/book/book.aspx?reqtyp=AIR&officeID=EMABD08ZZ&language=GB&market=UK&country=GB&ibeSource=ARC:BmiArcDevAccount&cityfrominput0=LHR&cit ytoinput0=MAN&oneway=1&day0=1&month0=9&fb_numpaxADT=2&fb_numpaxCHD=1&fb_numpaxINF=0',
                                                  'http://www.flybmi.com/book/book.aspx?reqtyp=AIR&officeID=EMABD08ZZ&language=GB&market=UK&country=GB&ibeSource=ARC:BmiArcDevAccount&cityfrominput0=LHR&citytoinput0=MAN&oneway=1&day0=1&month0=9&fb_numpaxADT=2&fb_numpaxCHD=1&fb_numpaxINF=0'
                                                 )
            )
            self.assertTrue(r['departure_datetime'] in (datetime.datetime(2008, 9, 1, 6, 55),
                                                        datetime.datetime(2008, 9, 1, 19, 20)
                                                       )
            )
            self.assertTrue(r['arrival_datetime']) in (datetime.datetime(2008, 9, 1, 20, 25),
                                                      datetime.datetime(2008, 9, 1, 8, 0))
            self.assertTrue(r['price'] in (132.0, 507.0))

class TestGetOutboundDates(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getOutboundDates_endInPast(self):
        self.assertEqual(search.getOutboundDates({'end_date':datetime.date.today()-datetime.timedelta(1)}), [])

    def test_getOutboundDates_normal(self):
        dates = search.getOutboundDates({'end_date': datetime.date.today()+datetime.timedelta(21),
                                         'start_date': datetime.date.today()-datetime.timedelta(7),
                                         'departdaysofweek': [1]})
        self.assertEqual(len(dates), 3)
        for d in dates:
            self.assertEqual(d.isoweekday(), 1)

    def test_getOutboundDates_multiple(self):
        dates = search.getOutboundDates({'end_date': datetime.date.today()+datetime.timedelta(21),
                                         'start_date': datetime.date.today()-datetime.timedelta(7),
                                         'departdaysofweek': [1, 3]})
        self.assertEqual(len(dates), 6)
        for d in dates:
            self.assertTrue(d.isoweekday() in (1,3))
        self.assertEqual(len([d for d in dates if d.isoweekday()==3]), 3)

class TestGetReturnDates(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getReturnDates_normal(self):
        today = datetime.date.today()
        result = search.getReturnDates(today, [7, 10, 14])
        self.assertEqual(len(result), 3)
        for x in (today+datetime.timedelta(7),
                  today+datetime.timedelta(10),
                  today+datetime.timedelta(14)):
            self.assertTrue(x in result)

class TestGetSearchCombos(unittest.TestCase):
    def setUp(self):
        self.getOutboundDates = search.getOutboundDates
        self.getReturnDates = search.getReturnDates
        search.getOutboundDates = mock.Mock()
        search.getReturnDates = mock.Mock()

    def tearDown(self):
        search.getOutboundDates = self.getOutboundDates
        search.getReturnDates = self.getReturnDates

    def test_getSearchCombos_normal(self):
        today = datetime.date.today()
        tomorrow = today+datetime.timedelta(1)
        search.getOutboundDates.return_value = [today, tomorrow]
        search.getReturnDates = lambda d, x: [d+datetime.timedelta(1), d+datetime.timedelta(2)]

        result = search.getSearchCombos({'origins': ['MAN','LHR'], 'destinations': ['ABR','ALC'], 'num_days':[1,2]})
        self.assertEqual(len(result), 8)
        for x in (((today, 'MAN', 'ABR'),[(tomorrow, 'ABR','MAN'),(tomorrow+datetime.timedelta(1), 'ABR','MAN')]),
                  ((tomorrow, 'MAN', 'ABR'),[(tomorrow+datetime.timedelta(1), 'ABR','MAN'),(tomorrow+datetime.timedelta(2), 'ABR','MAN')]),
                  ((today, 'MAN', 'ALC'),[(tomorrow, 'ALC','MAN'),(tomorrow+datetime.timedelta(1), 'ALC','MAN')]),
                  ((tomorrow, 'MAN', 'ALC'),[(tomorrow+datetime.timedelta(1), 'ALC','MAN'),(tomorrow+datetime.timedelta(2), 'ALC','MAN')]),
                  ((today, 'LHR', 'ABR'),[(tomorrow, 'ABR','LHR'),(tomorrow+datetime.timedelta(1), 'ABR','LHR')]),
                  ((tomorrow, 'LHR', 'ABR'),[(tomorrow+datetime.timedelta(1), 'ABR','LHR'),(tomorrow+datetime.timedelta(2), 'ABR','LHR')]),
                  ((today, 'LHR', 'ALC'),[(tomorrow, 'ALC','LHR'),(tomorrow+datetime.timedelta(1), 'ALC','LHR')]),
                  ((tomorrow, 'LHR', 'ALC'),[(tomorrow+datetime.timedelta(1), 'ALC','LHR'),(tomorrow+datetime.timedelta(2), 'ALC','LHR')])):
            try:
                self.assertTrue(x in result)
            except AssertionError:
                print "-----"
                pprint(x)
                print "not in result\n-----"
                raise

class TestPerformSearch(unittest.TestCase):
    def setUp(self):
        self.getSearchCombos = search.getSearchCombos
        self.getAvailability = search.getAvailability
        search.getSearchCombos = mock.Mock()
        search.getAvailability = mock.Mock()

    def tearDown(self):
        search.getSearchCombos = self.getSearchCombos
        search.getAvailability = self.getAvailability

    def test_performSearch_normal(self):
        today = datetime.date.today()
        search.getSearchCombos.return_value = [(
            (today, 'MAN', 'ALB'),
            [(today+datetime.timedelta(1), 'ALB','MAN'),
             (today+datetime.timedelta(2), 'ALB','MAN')]
            )]
        def getAvailability(date, *args, **kwargs):
            if date==today:
                # outbound
                return [{'departure_datetime': 'outbound_departure',
                         'arrival_datetime': 'outbound_arrival',
                         'num_changes': 0,
                         'price': 120.0,
                         'booking_link': ''}]
            if date==today+datetime.timedelta(1):
                # 1st return date
                return []
            if date==today+datetime.timedelta(2):
                # 2nd return date
                return [{'departure_datetime':'return1_departure',
                         'arrival_datetime': 'return1_arrival',
                         'num_changes': 0,
                         'price': 50.0,
                         'booking_link': ''},
                        {'departure_datetime': 'return2_departure',
                         'arrival_datetime': 'return2_arrival',
                         'num_changes': 0,
                         'price': 500.0,
                         'booking_link': ''}]
        search.getAvailability = getAvailability

        result = search.performSearch({'price': 200.0})

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['price'], 170.0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetAvailability())
    suite.addTest(TestGetOutboundDates())
    suite.addTest(TestGetReturnDates())
    suite.addTest(TestPerformSearch())
    suite.addTest(TestGetSearchCombos())
    return suite

if __name__ == '__main__':
    unittest.main()