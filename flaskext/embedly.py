# -*- coding: utf-8 -*-
"""
    flaskext.embedly
    ~~~~~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Matt Swanson.
    :license: BSD, see LICENSE for more details.
"""

import re
import urllib, urllib2
from flask import Markup

try:
    import json
except ImportError:
    import simplejson as json

API_VER = 'v1'
API_URL = 'http://api.embed.ly/%s/api/oembed?' % API_VER
API_ARGS = ['maxwidth', 'maxheight', 'format']

class Embedly(object):
    def __init__(self, app):
        app.jinja_env.filters['embedly'] = self._get_oembed

    def _get_oembed(self, url, **kwargs):
        params = { 'url' : url }

        for key, value in kwargs.items():
            if key not in API_ARGS:
                raise ValueError('Invalid Argument %s' % key)
            params[key] = value

        call_url = '%s%s' % (API_URL, urllib.urlencode(params))
        try:
            response = json.loads(urllib2.urlopen(call_url).read())
        except urllib2.HTTPError, e:
            return 'Embedly failed: %s' % e
        except urllib2.URLError, e:
            return 'Embedly failed: %s' % e

        return self._wrap_media(response)

    def _wrap_media(self, response):
        if response['type'] == u'photo':
            return Markup('<img src="%s" />' % response['url'])
        elif response['type'] == u'video':
            return Markup(response['html'])
        elif response['type'] == u'rich':
            #watch out for xss...
            return Markup(response['html'])
        else:
            return Markup('<a>%s</a>' % response['url'])



