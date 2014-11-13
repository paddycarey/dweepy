# -*- coding: utf-8 -*-

# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# local imports
from .api import DweepyError
from .api import dweet
from .api import dweet_for
from .api import get_alert
from .api import get_dweets_for
from .api import get_latest_dweet_for
from .api import lock
from .api import remove_alert
from .api import remove_lock
from .api import set_alert
from .api import unlock
from .streaming import listen_for_dweets_from


# all of the following objects will be imported if the caller does
# `from dweepy import *` (don't)
__all__ = [
    'DweepyError', 'dweet', 'dweet_for', 'get_alert', 'get_dweets_for',
    'get_latest_dweet_for', 'listen_for_dweets_from', 'lock', 'remove_alert',
    'remove_lock', 'set_alert', 'unlock',
]
