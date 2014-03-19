#!/usr/bin/env python
# -*- coding: utf-8 -*-

# marty mcfly imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import json

# third-party imports
import requests
from requests.exceptions import ChunkedEncodingError


__all__ = ['dweet', 'dweet_for', 'get_latest_dweet_for', 'get_dweets_for', 'listen_for_dweets_from']

# base url for all requests
BASE_URL = 'https://dweet.io'


def _request(method, url, **kwargs):
    """Make HTTP request, raising an exception if it fails.
    """
    url = BASE_URL + url
    request_func = getattr(requests, method)
    response = request_func(url, **kwargs)
    # raise an exception if request is not successful
    if not response.status_code == requests.codes.ok:
        response.raise_for_status()
    return response.json()


def _send_dweet(payload, url):
    """Send a dweet to dweet.io
    """
    data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    return _request('post', url, data=data, headers=headers)


def dweet(payload):
    """Send a dweet to dweet.io without naming your thing
    """
    return _send_dweet(payload, '/dweet')


def dweet_for(thing_name, payload):
    """Send a dweet to dweet.io for a thing with a known name
    """
    return _send_dweet(payload, '/dweet/for/{0}'.format(thing_name))


def get_latest_dweet_for(thing_name):
    """Read the latest dweet for a dweeter
    """
    return _request('get', '/get/latest/dweet/for/{0}'.format(thing_name))


def get_dweets_for(thing_name):
    """Read all the dweets for a dweeter
    """
    return _request('get', '/get/dweets/for/{0}'.format(thing_name))


def _reconnect_listen_request(wrapped_function):
    """Reconnect to the listen endpoint when the connection dies unexpectedly
    """
    def _arguments_wrapper(thing_name):
        while True:
            try:
                for x in wrapped_function(thing_name):
                    yield x
            except ChunkedEncodingError:
                pass
    return _arguments_wrapper


@_reconnect_listen_request
def listen_for_dweets_from(thing_name):
    """Create a real-time subscription to dweets
    """
    url = BASE_URL + '/listen/for/dweets/from/{0}'.format(thing_name)
    session = requests.Session()
    request = requests.Request("GET", url).prepare()
    resp = session.send(request, stream=True, timeout=900)

    streambuffer = ''
    for byte in resp.iter_content():
        if byte:
            streambuffer += byte
            try:
                dweet = json.loads(streambuffer)
            except ValueError:
                continue
            yield dweet
            streambuffer = ''
