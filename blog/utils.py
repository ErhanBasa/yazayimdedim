# -*- coding: utf-8 -*-

import requests
import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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


def send_mail_with_template(subject=None, mail_to=None, template=None, context={}):
    if not isinstance(mail_to, list):
        mail_to = [mail_to]

    body = render_to_string(template, context)
    email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, mail_to)
    email.content_subtype = 'html'
    return email.send()
