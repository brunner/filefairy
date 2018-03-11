#!/usr/bin/env python

import datetime

data = {
    'plugins': {
        'foo': {
            'date': datetime.datetime(1985, 10, 26, 0, 2, 30),
            'ok': True
        },
        'bar': {
            'date': datetime.datetime(1985, 10, 26, 0, 2, 35),
            'ok': True
        },
        'baz': {
            'date': datetime.datetime(1985, 10, 26, 0, 2, 40),
            'ok': False
        }
    }
}
