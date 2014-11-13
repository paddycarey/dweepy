#!/usr/bin/env python
# -*- coding: utf-8 -*-

# marty mcfly imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import datetime
import json

try:
    # python 3
    from urllib.parse import quote
except ImportError:
    # python 2
    from urllib import quote

# third-party imports
import requests
from requests.exceptions import ChunkedEncodingError


__all__ = ['dweet', 'dweet_for', 'get_latest_dweet_for', 'get_dweets_for', 'listen_for_dweets_from']

# base url for all requests
BASE_URL = 'https://dweet.io'


# python 2/3 compatibility shim for checking if value is a text type
try:
    basestring  # attempt to evaluate basestring

    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


class DweepyError(Exception):
    pass


def _request(method, url, **kwargs):
    """Make HTTP request, raising an exception if it fails.
    """
    url = BASE_URL + url
    request_func = getattr(requests, method)
    response = request_func(url, **kwargs)
    # raise an exception if request is not successful
    if not response.status_code == requests.codes.ok:
        raise DweepyError('HTTP {0} response'.format(response.status_code))
    response_json = response.json()
    if response_json['this'] == 'failed':
        raise DweepyError(response_json['because'])
    return response_json['with']


def _send_dweet(payload, url, params=None):
    """Send a dweet to dweet.io
    """
    data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    return _request('post', url, data=data, headers=headers, params=params)


def dweet(payload):
    """Send a dweet to dweet.io without naming your thing
    """
    return _send_dweet(payload, '/dweet')


def dweet_for(thing_name, payload, key=None):
    """Send a dweet to dweet.io for a thing with a known name
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _send_dweet(payload, '/dweet/for/{0}'.format(thing_name), params=params)


def get_latest_dweet_for(thing_name, key=None):
    """Read the latest dweet for a dweeter
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _request('get', '/get/latest/dweet/for/{0}'.format(thing_name), params=params)


def get_dweets_for(thing_name, key=None):
    """Read all the dweets for a dweeter
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _request('get', '/get/dweets/for/{0}'.format(thing_name), params=params)


def _check_stream_timeout(started, timeout):
    """Check if the timeout has been reached and raise a `StopIteration` if so.
    """
    if timeout:
        elapsed = datetime.datetime.utcnow() - started
        if elapsed.seconds > timeout:
            raise StopIteration


def _listen_for_dweets_from_response(response):
    """Yields dweets as received from dweet.io's streaming API
    """
    streambuffer = ''
    for byte in response.iter_content():
        if byte:
            streambuffer += byte.decode('ascii')
            try:
                dweet = json.loads(streambuffer.splitlines()[1])
            except (IndexError, ValueError):
                continue
            if isstr(dweet):
                yield json.loads(dweet)
            streambuffer = ''


def listen_for_dweets_from(thing_name, timeout=900, key=None):
    """Create a real-time subscription to dweets
    """
    url = BASE_URL + '/listen/for/dweets/from/{0}'.format(thing_name)
    session = requests.Session()
    if key is not None:
        params = {'key': key}
    else:
        params = None

    start = datetime.datetime.utcnow()
    while True:
        request = requests.Request("GET", url, params=params).prepare()
        resp = session.send(request, stream=True, timeout=timeout)
        try:
            for x in _listen_for_dweets_from_response(resp):
                yield x
                _check_stream_timeout(start, timeout)
        except (ChunkedEncodingError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            pass
        _check_stream_timeout(start, timeout)


def remove_lock(lock, key):
    """Remove a lock (no matter what it's connected to).
    """
    return _request('get', '/remove/lock/{0}'.format(lock), params={'key': key})


def lock(thing_name, lock, key):
    """Lock a thing (prevents unauthed dweets for the locked thing)
    """
    return _request('get', '/lock/{0}'.format(thing_name), params={'key': key, 'lock': lock})


def unlock(thing_name, key):
    """Unlock a thing
    """
    return _request('get', '/unlock/{0}'.format(thing_name), params={'key': key})


def set_alert(thing_name, who, condition, key):
    """Set an alert on a thing with the given condition
    """
    return _request('get', '/alert/{0}/when/{1}/{2}'.format(
        ','.join(who),
        thing_name,
        quote(condition),
    ), params={'key': key})


def get_alert(thing_name, key):
    """Set an alert on a thing with the given condition
    """
    return _request('get', '/get/alert/for/{0}'.format(thing_name), params={'key': key})


def remove_alert(thing_name, key):
    """Remove an alert for the given thing
    """
    return _request('get', '/remove/alert/for/{0}'.format(thing_name), params={'key': key})
