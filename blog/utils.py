# -*- coding: utf-8 -*-

import requests
import json
from django.conf import settings

def get_count(api, url):
    """
        using twitter or facebook api brings the total number of sharing.
        get_count(<facebook or twitter>, <url>)
    """
    social = settings.APIS[api]
    r  = requests.get(social['url'] + url)
    data = r.text
    if social['key'] in json.loads(data):
        return json.loads(data)[social['key']]
    return 0
