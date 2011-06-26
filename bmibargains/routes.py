import datetime
import urllib

from lxml import etree
from repoze.bfg.renderers import render

import config

def getRoutes(root):
    """ @return a list of routes

    """

    routes_cache = getattr(root,'routes_cache',None)
    if config.USE_CACHE and routes_cache and \
       (datetime.datetime.now()-routes_cache[1])<datetime.timedelta(hours=config.EXPIRE_CACHE):
        return routes_cache[0]

    request = render('bmibargains:templates/GetRoutesRequest.pt',
                     {'guid': config.GUID})
    request = urllib.urlencode({'requestMessage': request})
    request_url = '%s/GetRoutes' % (config.API_URL,)
    try:
        response = urllib.urlopen(request_url, request).read()
    except:
        # TODO: be more specific
        return {}
    try:
        response = etree.fromstring(response).text
        response = etree.fromstring(response)
    except:
        # TODO: be more specific
        return {}
    # TODO: check for success tag
    routes = []
    for route in response.xpath('//Route'):
        routes.append((route.get('FromCode'), route.get('ToCode')))

    routes_dict = {}
    for k, v in routes:
        if k not in routes_dict:
            routes_dict[k] = []
        routes_dict[k].append(v)

    routes = routes_dict

    if config.USE_CACHE:
        root.routes_cache = (routes, datetime.datetime.now())

    return routes