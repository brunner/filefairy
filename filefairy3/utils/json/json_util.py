#!/usr/bin/env python

import json


def dumps(data):
    return json.dumps(data, indent=2, sort_keys=True)
