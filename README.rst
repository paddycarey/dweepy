===============================
Dweepy
===============================


Dweepy is a simple Python client for dweet.io

* Free software: MIT license
* Documentation: https://github.com/paddycarey/dweepy



Installation
------------

Distribute & Pip
~~~~~~~~~~~~~~~~

Installing dweepy is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install dweepy

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install dweepy

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.


Get the Code
~~~~~~~~~~~~

Dweepy is actively developed on GitHub, where the code is `always available <https://github.com/paddycarey/dweepy>`_.

You can either clone the public repository::

    $ git clone git://github.com/paddycarey/dweepy.git

Or download the `tarball <https://github.com/paddycarey/dweepy/tarball/master>`_::

    $ curl -OL https://github.com/paddycarey/dweepy/tarball/master

Once you have a copy of the source, you can embed it in your Python package, or install it into your site-packages easily::

    $ python setup.py install



Usage
-----

Dweepy aims to provide a simple, pythonic interface to dweet.io. It has been designed to be easy to use, and aims to cover the dweet.io API entirely.

First you'll need to import dweepy.::

    import dweepy


Dweeting
~~~~~~~~

You can send a dweet without specify a name for your thing.::

    >>> dweepy.dweet({'some_key': 'some_value'})
    {
        u'by': u'dweeting',
        u'the': u'dweet',
        u'this': u'succeeded',
        u'with': {
            u'content': {u'some_key': u'some_value'},
            u'created': u'2014-03-19T10:35:59.504Z',
            u'thing': u'unequaled-start'
        }
    }

Note: If you do not specify a name for your thing, dweet.io will assign a random name and return it in the response as above.

You can send a dweet from a thing with a specified name.::

    >>> dweepy.dweet_for('this_is_a_thing', {'some_key': 'some_value'})
    {
        u'by': u'dweeting',
        u'the': u'dweet',
        u'this': u'succeeded',
        u'with': {
            u'content': {u'some_key': u'some_value'},
            u'created': u'2014-03-19T10:38:46.010Z',
            u'thing': u'this_is_a_thing'
        }
    }



Getting Dweets
~~~~~~~~~~~~~~

To read the latest dweet for a dweeter, you can call::

    >>> dweepy.get_latest_dweet_for('this_is_a_thing')
    {
        u'by': u'getting',
        u'the': u'dweets',
        u'this': u'succeeded',
        u'with': [
            {
                u'content': {u'some_key': u'some_value'},
                u'created': u'2014-03-19T10:38:46.010Z',
                u'thing': u'this_is_a_thing'
            }
        ]
    }

Note that dweet.io only holds on to the last 500 dweets over a 24 hour period. If the thing hasn't dweeted in the last 24 hours, its history will be removed.

Or to read all the dweets for a dweeter, you can call::

    >>> dweepy.get_dweets_for('this_is_a_thing')
    {
        u'by': u'getting',
        u'the': u'dweets',
        u'this': u'succeeded',
        u'with': [
            {
                u'content': {u'some_key': u'some_value'},
                u'created': u'2014-03-19T10:42:31.316Z',
                u'thing': u'this_is_a_thing'
            },
            {
                u'content': {u'some_key': u'some_value'},
                u'created': u'2014-03-19T10:38:46.010Z',
                u'thing': u'this_is_a_thing'
            }
        ]
    }



Subscriptions & Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


You can create a real-time subscription to dweets using a "chunked" HTTP response.::

    >>> for dweet in dweepy.listen_for_dweets_from('this_is_a_thing'):
    >>>     print dweet
    {u'content': {u'some_key': u'some_value'}, u'thing': u'this_is_a_thing', u'created': u'2014-03-19T10:45:28.934Z'}
    {u'content': {u'some_key': u'some_value'}, u'thing': u'this_is_a_thing', u'created': u'2014-03-19T10:45:31.574Z'}

The server will keep the connection alive and send you dweets as they arrive.



TODO
----

* Switch to socket.io for streaming support as in official JS client
* add `lock <https://dweet.io/locks>`_ support
