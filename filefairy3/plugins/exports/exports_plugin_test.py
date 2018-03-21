#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import mock
import os
import re
import unittest
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from plugins.exports.exports_plugin import ExportsPlugin  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import TestUtil  # noqa

DATA = ExportsPlugin._data()
EXPORTS_NEW = [('31', 'New'), ('32', 'Old')]
EXPORTS_OLD = [('31', 'Old'), ('32', 'Old')]
FILE_DATE_NEW = 'Sunday February 4, 2018 20:42:30 EST'
FILE_DATE_OLD = 'Friday February 2, 2018 19:53:16 EST'
TEAM_CANONICAL = {'ai': False, 'form': '', 'n': 0, 'o': 0}
TEAM_TRUNCATED = {'ai': False, 'form': 'nonnnonnno', 'n': 15, 'o': 5}
TEAM_NEW = {'ai': False, 'form': 'n', 'n': 1, 'o': 0}
TEAM_NEW_TRUNCATED = {'ai': False, 'form': 'onnnonnnon', 'n': 16, 'o': 5}
TEAM_OLD = {'ai': False, 'form': 'o', 'n': 0, 'o': 1}
TEAM_OLD_TRUNCATED = {'ai': False, 'form': 'onnnonnnoo', 'n': 15, 'o': 6}
URL = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
URLOPEN = '<html><head><title>Export Tracker - StatsLab for ...'


class ExportsPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'apis.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()
        patch_urlopen = mock.patch('plugins.exports.exports_plugin.urlopen')
        self.addCleanup(patch_urlopen.stop)
        self.mock_urlopen = patch_urlopen.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_urlopen.return_value = URLOPEN

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_urlopen.reset_mock()

    def create_plugin(self, data, file_date='', exports=[]):
        self.init_mocks(data)
        plugin = ExportsPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if file_date:
            plugin.file_date = file_date
        if exports:
            plugin.exports = exports

        return plugin

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_setup(self, mock_exports, mock_file_date):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = EXPORTS_OLD

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read)
        plugin._setup()

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_called_once_with(URLOPEN)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__empty_file_date(self, mock_exports, mock_file_date):
        mock_file_date.return_value = ''
        mock_exports.return_value = []

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._run_internal()
        self.assertFalse(ret)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__empty_self_file_date(self, mock_exports, mock_file_date):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = []

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read, file_date='', exports=EXPORTS_OLD)
        plugin.file_date = ''
        ret = plugin._run_internal()
        self.assertFalse(ret)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__new_file_date_canonical(self, mock_exports, mock_file_date):
        mock_file_date.return_value = FILE_DATE_NEW
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_NEW)
        ret = plugin._run_internal()
        self.assertTrue(ret)

        write = {'31': TEAM_NEW, '32': TEAM_OLD}
        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_NEW)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__new_file_date_truncated(self, mock_exports, mock_file_date):
        mock_file_date.return_value = FILE_DATE_NEW
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_TRUNCATED) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_NEW)
        ret = plugin._run_internal()
        self.assertTrue(ret)

        write = {'31': TEAM_NEW_TRUNCATED, '32': TEAM_OLD_TRUNCATED}
        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_NEW)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__old_file_date(self, mock_exports, mock_file_date):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._run_internal()
        self.assertFalse(ret)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_called_once_with(URLOPEN)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    def test_file_date__with_valid_input(self):
        text = '<td>League File Updated: Sunday May 4, 2018 20:42:30 EST</td>'
        actual = ExportsPlugin._file_date(text)
        expected = 'Sunday May 4, 2018 20:42:30 EST'
        self.assertEqual(actual, expected)

    def test_file_date__with_invalid_input(self):
        text = '<td></td>'
        actual = ExportsPlugin._file_date(text)
        expected = ''
        self.assertEqual(actual, expected)

    def test_exports__with_valid_input(self):
        text = '<td><a href="../teams/team_36.html">Chicago Cubs</a>' + \
               '<br><span>February 3, 2018<br>New Export</span></td>' + \
               '<td><a href="../teams/team_37.html">Cincinnati Reds</a>' + \
               '<br><span>February 3, 2018<br>Old Export</span></td>'
        actual = ExportsPlugin._exports(text)
        expected = [('36', 'New'), ('37', 'Old')]
        self.assertEqual(actual, expected)

    def test_exports__with_invalid_input(self):
        text = '<td></td>'
        actual = ExportsPlugin._exports(text)
        expected = []
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
