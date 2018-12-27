#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for testing other modules."""

import abc
import importlib
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/test', '', _path))

from api.renderable.renderable import Renderable  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa

ISO = 'iso-8859-1'


class Mock(object):
    def __init__(self, read=None, write=None):
        self.mo = mock.mock_open(read_data=read)
        self.mock_handle = self.mo()
        self.write = write


class RMock(Mock):
    def __init__(self, path, filename, testdata):
        self.call = mock.call(os.path.join(path, filename), 'r', encoding=ISO)
        super().__init__(read=testdata[filename])


class WMock(Mock):
    def __init__(self, path, filename, testdata):
        self.call = mock.call(os.path.join(path, filename), 'w')
        super().__init__(write=testdata[filename])


class Suite(object):
    def __init__(self, *mocks):
        self.mocks = mocks

    def calls(self):
        return [m.call for m in self.mocks]

    def values(self):
        return [m.mo.return_value for m in self.mocks]

    def verify(self):
        for m in self.mocks:
            if m.write is not None:
                m.mock_handle.write.assert_called_once_with(m.write)


class Test(unittest.TestCase):
    @abc.abstractmethod
    def init_mocks(self):
        pass

    def assertNotCalled(self, *mocks):
        for m in mocks:
            m.assert_not_called()


def _gen_golden(case, _cls, _pkg, _pth, _read, **kwargs):
    @mock.patch.object(_cls, '_render_data')
    def test_golden(self, mock_render):
        self.init_mocks(_read)

        date = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)
        golden = os.path.join(_pth, 'goldens/{}.html'.format(case))
        sample = '{}.samples.{}'.format(_pkg, case)
        module = importlib.import_module(sample)
        subtitle, tmpl, context = [
            getattr(module, attr) for attr in ['subtitle', 'tmpl', 'context']
        ]
        mock_render.return_value = [(golden, subtitle, tmpl, context)]

        renderable = _cls(**kwargs)
        renderable._render(date=date, test=True)

    return test_golden


def get_testdata(path):
    testdata = {}
    for name in os.listdir(path):
        if name == '__init__.py':
            continue
        filename = os.path.join(path, name)
        if os.path.isfile(filename):
            testdata[name] = open(filename, 'r', encoding=ISO).read()

    return testdata


def main(_tst, _cls, _pkg, _pth, _read, _main, **kwargs):
    if issubclass(_cls, Renderable):
        root = re.sub(r'/common/test', '', _path)
        d = os.path.join(root, _pth, 'samples')

        for c in filter(lambda x: '_' not in x, os.listdir(d)):
            case = re.sub('.py', '', c)
            test_golden = _gen_golden(case, _cls, _pkg, _pth, _read, **kwargs)
            setattr(_tst, 'test_golden__{}'.format(case), test_golden)

    if _main:
        unittest.main()
