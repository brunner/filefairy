#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class Encoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return ''


def dumps(data):
    return json.dumps(data, indent=2, sort_keys=True, cls=Encoder)
