#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import urllib.error as error
import urllib.parse as parse
import urllib.request as request

logger_ = logging.getLogger('filefairy')


def urlopen(url, params={}):
    try:
        data = parse.urlencode(params).encode('utf-8')
        with request.urlopen(url, data=data, timeout=10) as f:
            return f.read()
    except error.HTTPError as e:
        if e.code not in [403, 404]:
            logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
        return b''
    except:
        logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
        return b''
