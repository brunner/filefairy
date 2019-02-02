#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests

_logger = logging.getLogger('filefairy')


def get(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == requests.codes.ok:
            return r.text
    except Exception:
        _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
    return ''
