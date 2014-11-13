===============================
Dweepy
===============================

.. image:: https://img.shields.io/pypi/v/dweepy.svg?style=flat
    :target: https://pypi.python.org/pypi/dweepy/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/dweepy.svg?style=flat
    :target: https://pypi.python.org/pypi/dweepy/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/paddycarey/dweepy/master.png?style=flat
    :target: https://travis-ci.org/paddycarey/dweepy
    :alt: Travis CI build status

Dweepy is a simple Python client for `dweet.io <https://dweet.io>`_. Dweepy has a full test suite and aims to have 100% coverage of the `dweet.io <https://dweet.io>`_ API (we're pretty much there already).

Large portions of this README have been adapted from the README of the the official `javascript client from buglabs <https://github.com/buglabs/dweetio-client/blob/master/README.md>`_.

Dweepy supports Python 2.6, 2.7, PyPy, 3.3 and 3.4 (and probably later versions too, but I haven't tested on those).

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
        u'content': {u'some_key': u'some_value'},
        u'created': u'2014-03-19T10:35:59.504Z',
        u'thing': u'unequaled-start'
    }

Note: If you do not specify a name for your thing, dweet.io will assign a random name and return it in the response as above.

You can send a dweet from a thing with a specified name.::

    >>> dweepy.dweet_for('this_is_a_thing', {'some_key': 'some_value'})
    {
        u'content': {u'some_key': u'some_value'},
        u'created': u'2014-03-19T10:38:46.010Z',
        u'thing': u'this_is_a_thing'
    }


Getting Dweets
~~~~~~~~~~~~~~

To read the latest dweet for a thing, you can call::

    >>> dweepy.get_latest_dweet_for('this_is_a_thing')
    [
        {
            u'content': {u'some_key': u'some_value'},
            u'created': u'2014-03-19T10:38:46.010Z',
            u'thing': u'this_is_a_thing'
        }
    ]


Note that dweet.io only holds on to the last 500 dweets over a 24 hour period. If the thing hasn't dweeted in the last 24 hours, its history will be removed.

Or to read all the dweets for a thing, you can call::

    >>> dweepy.get_dweets_for('this_is_a_thing')
    [
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


Alerts
~~~~~~

Set an alert::

    >>> dweepy.set_alert(
    ...     'this_is_a_thing',
    ...     ['test@example.com', 'anothertest@example.com'],
    ...     "if(dweet.alertValue > 10) return 'TEST: Greater than 10'; if(dweet.alertValue < 10) return 'TEST: Less than 10';",
    ...     'this-is-a-key',
    ... )
    {
        u'thing': u'this_is_a_thing',
        u'condition': u"if(dweet.alertValue > 10) return 'TEST: Greater than 10'; if(dweet.alertValue < 10) return 'TEST: Less than 10';",
        u'is_demo': False,
        u'recipients': [
            {
                u'type': u'email',
                u'address': u'test@example.com',
            },
            {
                u'type': u'email',
                u'address': u'anothertest@example.com',
            }
        ]
    }


Get an alert (with status)::

    >>> dweepy.get_alert('this_is_a_thing', 'this-is-a-key')
    {
        u'status': {
            u'message': u'',
            u'since': None,
            u'open': False,
            u'alerts_sent_today': 0,
            u'alerts_allowed_today': 100,
        },
        u'thing': u'this_is_a_thing',
        u'condition': u"if(dweet.alertValue > 10) return 'TEST: Greater than 10'; if(dweet.alertValue < 10) return 'TEST: Less than 10';",
        u'is_demo': False,
        u'recipients': [
            {
                u'type': u'email',
                u'address': u'test@example.com'
            },
            {
                u'type': u'email',
                u'address': u'anothertest@example.com'
            }
        ]
    }


Remove an alert::

    >>> dweepy.remove_alert('this_is_a_thing', 'this-is-a-key')
    {
        u'thing': u'this_is_a_thing'
    }


Subscriptions & Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


You can create a real-time subscription to dweets using a "chunked" HTTP response.::

    >>> for dweet in dweepy.listen_for_dweets_from('this_is_a_thing'):
    >>>     print dweet
    {u'content': {u'some_key': u'some_value'}, u'thing': u'this_is_a_thing', u'created': u'2014-03-19T10:45:28.934Z'}
    {u'content': {u'some_key': u'some_value'}, u'thing': u'this_is_a_thing', u'created': u'2014-03-19T10:45:31.574Z'}

The server will keep the connection alive and send you dweets as they arrive.


Locking & Security
~~~~~~~~~~~~~~~~~~

By default, all things are publicly accessible if you know the name of the thing. You can also lock things so that they are only accessible to users with valid security credentials. To purchase locks, visit `https://dweet.io/locks <https://dweet.io/locks>`_. The locks will be emailed to you.


To lock a thing::

    >>> dweepy.lock("my-thing", "my-lock", "my-key")


To unlock a thing::

    >>> dweepy.unlock("my-thing", "my-key")
    "my-thing"


To remove a lock no matter what it's attached to::

    >>> dweepy.remove_lock("my-lock", "my-key")
    "my-lock"


Once a thing has been locked, you must pass the key to the lock with any call you make to other functions in this client library. The key will be passed as an optional keyword argument. For example::

    >>> dweepy.dweet_for("my-locked-thing", {"some":"data"}, "my-key")
    >>> dweepy.get_latest_dweet_for("my-locked-thing", "my-key")
    >>> dweepy.get_dweets_for("my-locked-thing", "my-key")
    >>> dweepy.listen_for_dweets_from("my-locked-thing", "my-key")

Failure to pass a key or passing an incorrect key for a locked thing will result in an exception being raised.


Error Handling
~~~~~~~~~~~~~~

When dweepy encounters an error a ``DweepyError`` exception is raised. This can happen either when a HTTP request to the dweet.io API fails with an invalid status code, or if the HTTP request succeeds but the request fails for some reason (invalid key, malformed request data, invalid action etc.).


Testing
-------

Dweepy has a full test suite (a port of `dweetio-client's <https://github.com/buglabs/dweetio-client>`_ test suite). Assuming you have a full source checkout of the dweepy repository, running the tests is simple with ``tox``::

    $ pip install tox
    $ tox

It is recommended that you use a virtualenv when developing or running the tests to ensure that system libraries do not interfere with the tests.

**NOTE:** In order for all of the tests to complete successfully you must set several environment variables. There are numerous ways to accomplish this, but I like `forego <https://github.com/ddollar/forego>`_ (a golang port of the `foreman <https://github.com/ddollar/foreman>`_ utility).

To use forego in your tests you should first create a ``.env`` file in the root of your repository with the following contents::

    DWEET_LOCK=mylock
    DWEET_KEY=mykey

Once in place, you can run your tests locally with::

    $ forego run tox

If you want to test against a single python version, you can use ``tox -e`` e.g.::

    $ forego run tox -e py27
    $ forego run tox -e pypy
    $ forego run tox -e py34

**TIP:** If you're using Ubuntu, you can find older/newer versions of python than the one shipped with your distribution `here <https://launchpad.net/~fkrull/+archive/ubuntu/deadsnakes>`_. You can install as many as you like side by side without affecting your default python install.


Copyright & License
-------------------

| Copyright © 2014 Patrick Carey (https://github.com/paddycarey)
| Licensed under the **MIT** license.
