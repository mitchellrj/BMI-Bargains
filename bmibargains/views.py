import datetime
from email.message import Message
import itertools
import random
import re
import string
import urllib

from repoze.bfg.renderers import render
from repoze.sendmail.delivery import DirectMailDelivery
from repoze.sendmail.mailer import SMTPMailer
import transaction

import config
from models import Search
from routes import getRoutes

def validate_new_search(email, start_date, end_date, departdaysofweek,
                        origins, destinations, min_days, max_days, price,
                        adults, children, infants):
    errors = {}

    if not re.search(config.EMAIL_RE, email):
            errors['email'] = 'Invalid email address'

    try:
        start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
    except:
        errors['start_date'] = 'Invalid start date'

    try:
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()

        if end_date<datetime.date.today():
            errors['end_date'] = 'End date must be in the future'

        if end_date<=start_date:
            errors['end_date'] = 'End date must be after the start date'
    except:
        errors['end_date'] = 'Invalid end date'

    if not departdaysofweek:
        errors['departdaysofweek'] = 'You must select some days on which you want to travel'

    if isinstance(departdaysofweek, basestring):
        departdaysofweek = [departdaysofweek,]

    try:
        departdaysofweek = [int(d) for d in departdaysofweek]

        if max(departdaysofweek)>7 or min(departdaysofweek)<1:
            raise ValueError
    except:
        errors.setdefault('departdaysofweek', 'Invalid day of the week entered')

    if not origins:
        errors['origins'] = 'You must select some airports from which you want to fly'

    if isinstance(origins, basestring):
        origins = [origins,]

    for o in origins:
        # TODO: check against routes
        if o not in config.IATA_CODE_MAP:
            errors.setdefault('origins', 'Some invalid airport selected')

    if not destinations:
        errors['destinations'] = 'You must select some airports from which you want to fly'

    if isinstance(destinations, basestring):
        destinations = [destinations,]

    for d in destinations:
        # TODO: check against routes
        if d not in config.IATA_CODE_MAP:
            errors.setdefault('destinations', 'Some invalid airport selected')

    if not min_days:
        errors['min_days'] = 'You must select some number of days to travel for'

    try:
        min_days = int(min_days)
        if min_days <= 0:
            errors.setdefault('min_days', 'You must travel for at least one day')
    except:
        errors.setdefault('min_days', 'Invalid number of days selected')

    if not max_days:
        errors['max_days'] = 'You must select some maximum number of days to travel for'

    try:
        max_days = int(max_days)
        if max_days-min_days > 14:
            errors.setdefault('max_days', 'Sorry, we cannot search for ranges of days greater than 2 weeks right now')
    except:
        errors.setdefault('max_days', 'Invalid number of days selected')

    num_days = []
    if not errors.get('min_days') and not errors.get('max_days'):
        num_days = range(min_days, max_days+1)

    if not price:
        errors['price'] = 'You must enter a maximum price you are willing to pay'

    try:
        price = float(price)
        if price <= 0.0:
            errors.setdefault('price', 'You\'ve gotta be willing to pay SOMETHING!')
    except:
        errors.setdefault('price', 'Invalid price entered')

    try:
        adults = int(adults)
    except:
        adults = 0
        errors.setdefault('adults', 'Invalid number of adults entered')

    try:
        children = int(children)
    except:
        children = 0
        errors.setdefault('children', 'Invalid number of children entered')

    try:
        infants = int(infants)
    except:
        infants = 0
        errors.setdefault('infants', 'Invalid number of infants entered')

    if adults+children+infants < 1:
        msg = "You must choose some number of people to travel"
        errors.setdefault('adults', msg)
        errors.setdefault('children', msg)
        errors.setdefault('infants', msg)

    return (email, start_date, end_date, departdaysofweek,
            origins, destinations, num_days, price, adults,
            children, infants), errors

def sendAddEmail(request, email, hash, destinations):
    mailer = SMTPMailer(port=config.SMTP_PORT)
    delivery = DirectMailDelivery(mailer)
    human_destinations = [config.IATA_CODE_MAP[d] for d in destinations]
    if len(human_destinations)>1:
        human_destinations = '%s and %s' % (', '.join(human_destinations[:-1]),
                                            human_destinations[-1])
    elif len(human_destinations)==1:
        human_destinations = human_destinations[0]

    confirm_link = request.relative_url('confirm?email=%s&code=%s' %
                                        (urllib.quote(email),
                                         urllib.quote(hash))
                                        )
    message_text = config.EMAIL_CONFIRM % \
                       {'destinations': human_destinations,
                        'confirm_link': confirm_link}
    message = Message()
    message.set_payload(message_text)
    delivery.send(config.FROM_ADDR, [email,], message)

def default(request):
    errors = {}
    added = False
    routes = getRoutes(request.root)
    if 'form.submitted' in request.POST:
        # validate
        email = request.POST.get('email', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        departdaysofweek = request.POST.getall('departdaysofweek')
        origins = request.POST.getall('origins')
        destinations = request.POST.getall('destinations')
        min_days = request.POST.get('min_days', '0')
        max_days = request.POST.get('max_days', '0')
        price = request.POST.get('price', '0.0')
        adults = request.POST.get('adults', '0')
        children = request.POST.get('children', '0')
        infants = request.POST.get('infants', '0')

        (email, start_date, end_date, departdaysofweek,
         origins, destinations, num_days, price, adults,
         children, infants), errors = \
            validate_new_search(email, start_date, end_date, departdaysofweek,
                                origins, destinations, min_days, max_days, price,
                                adults, children, infants)

        if not errors:
            random.seed()
            hash = ''
            while True:
                hash = ''.join(random.choice(string.hexdigits[:16]) for dummy in xrange(32))
                if hash not in request.root:
                    break
            request.root[hash] = Search(email, start_date, end_date,
                                        departdaysofweek, origins,
                                        destinations, num_days, price,
                                        adults, children, infants)
            transaction.commit()

            sendAddEmail(request, email, hash, destinations)

            added = True

    origins = routes.keys()
    destinations = []
    for v in routes.values():
        destinations.extend(v)
    destinations = set(destinations)
    return {'errors': errors, 'added': added, 'origins': origins,
            'destinations': destinations, 'route_code_map': config.IATA_CODE_MAP}

def remove(request):
    success = False
    if 'email' in request.GET and 'code' in request.GET and \
        request.GET['code'] in request.root and \
        request.root.get(request.GET['code'])['email'].lower()==request.GET['email'].lower():

        del request.root[request.GET['code']]
        success = True

    return {'success':success}

def confirm(request):
    success = False
    if 'email' in request.GET and 'code' in request.GET and \
        request.GET['code'] in request.root and \
        request.root.get(request.GET['code'])['email'].lower()==request.GET['email'].lower():

        request.root[request.GET['code']].activate()
        success = True

    return {'success':success}
