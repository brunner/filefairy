#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging

logger_ = logging.getLogger('fairylab')


class Encoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
            return ''


def dumps(data):
    return json.dumps(data, indent=2, sort_keys=True, cls=Encoder)
