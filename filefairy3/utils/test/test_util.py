#!/usr/bin/env python

import datetime
import importlib
import json
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/test', '', _path))
from apis.renderable.renderable_api import RenderableApi  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa


class TestUtil(unittest.TestCase):
    def write(self, fname, data):
        with open(fname, 'r+') as f:
            original = json.loads(f.read())
            f.seek(0)
            f.write(dumps(data))
            f.write('\n')
            f.truncate()
            return original


def _gen_golden(case, _cls, _pkg, _pth):
    @mock.patch.object(_cls, '_render_internal')
    @mock.patch.object(_cls, '_html')
    @mock.patch('apis.renderable.renderable_api.datetime')
    @mock.patch('apis.renderable.renderable_api.check_output')
    def test_golden(self, mock_check, mock_datetime, mock_html, mock_render):
        now = datetime.datetime(1985, 10, 26, 6, 2, 30)
        mock_datetime.datetime.now.return_value = now
        golden = os.path.join(_pth, 'goldens/{}_golden.html'.format(case))
        mock_html.return_value = golden
        sample = '{}.samples.{}_sample'.format(_pkg, case)
        module = importlib.import_module(sample)
        mock_render.return_value = getattr(module, 'sample')
        plugin = _cls(e=env())
        plugin._render()

    return test_golden


def main(_tst, _cls, _pkg, _pth):
    if issubclass(_cls, RenderableApi):
        d = os.path.join(_pth, 'samples')
        cs = filter(lambda x: x.endswith('_sample.py'), os.listdir(d))
        for c in cs:
            case = re.sub('_sample.py', '', c)
            test_golden = _gen_golden(case, _cls, _pkg, _pth)
            setattr(_tst, 'test_golden__{}'.format(case), test_golden)

    unittest.main()
