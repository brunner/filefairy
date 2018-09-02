#!/usr/bin/env pythonutils
# -*- coding: utf-8 -*-

import abc
import json
import importlib
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/test', '', _path)
sys.path.append(_root)
from api.renderable.renderable import Renderable  # noqa
from util.datetime_.datetime_ import datetime_datetime  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa


class Test(unittest.TestCase):
    @abc.abstractmethod
    def init_mocks(self):
        pass

    @staticmethod
    def write(fname, data):
        with open(fname, 'r+') as f:
            original = json.loads(f.read())
            f.seek(0)
            f.write(dumps(data) + '\n')
            f.truncate()
            return original


def _gen_golden(case, _cls, _pkg, _pth, _read, **kwargs):
    @mock.patch.object(_cls, '_render_internal')
    def test_golden(self, mock_render):
        self.init_mocks(_read)
        date = datetime_datetime(1985, 10, 26, 6, 2, 30)
        golden = os.path.join(_pth, 'goldens/{}.html'.format(case))
        sample = '{}.samples.{}'.format(_pkg, case)
        module = importlib.import_module(sample)
        subtitle, tmpl, context = [
            getattr(module, attr) for attr in ['subtitle', 'tmpl', 'context']
        ]
        mock_render.return_value = [(golden, subtitle, tmpl, context)]
        plugin = _cls(**kwargs)
        plugin._render(date=date, test=True)

    return test_golden


def main(_tst, _cls, _pkg, _pth, _read, _main, **kwargs):
    if issubclass(_cls, Renderable):
        d = os.path.join(_root, _pth, 'samples')
        cs = filter(lambda x: '_' not in x, os.listdir(d))
        for c in cs:
            case = re.sub('.py', '', c)
            test_golden = _gen_golden(case, _cls, _pkg, _pth, _read, **kwargs)
            setattr(_tst, 'test_golden__{}'.format(case), test_golden)

    if _main:
        unittest.main()
