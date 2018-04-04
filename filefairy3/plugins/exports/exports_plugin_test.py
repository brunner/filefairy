#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/exports', '', _path))
from plugins.exports.exports_plugin import ExportsPlugin  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.component.component_util import table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import main, TestUtil  # noqa

DATA = ExportsPlugin._data()
EXPORTS_NEW = [('31', 'New'), ('32', 'Old')]
EXPORTS_OLD = [('31', 'Old'), ('32', 'Old')]
FILE_DATE_NEW = 'Sunday February 4, 2018 20:42:30 EST'
FILE_DATE_OLD = 'Friday February 2, 2018 19:53:16 EST'
HOME = {'breadcrumbs': [], 'table': {}}
INDEX = 'html/fairylab/exports/index.html'
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
TEAM_CANONICAL = {'ai': False, 'form': '', 'streak': ''}
TEAM_TRUNCATED = {'ai': False, 'form': 'nonnnonnno', 'streak': '1o'}
TEAM_NEW = {'ai': False, 'form': 'n', 'streak': '1n'}
TEAM_NEW_TRUNCATED = {'ai': False, 'form': 'onnnonnnon', 'streak': '1n'}
TEAM_OLD = {'ai': False, 'form': 'o', 'streak': '1o'}
TEAM_OLD_TRUNCATED = {'ai': False, 'form': 'onnnonnnoo', 'streak': '2o'}
THEN = datetime.datetime(1985, 10, 26, 0, 0, 0)
URL = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
URLOPEN = '<html><head><title>Export Tracker - StatsLab for ...'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Exports'
}]


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

    def test_notify(self):
        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read)
        plugin._notify_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()

    def test_on_message(self):
        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__empty_file_date(self, mock_exports, mock_file_date,
                                  mock_render):
        mock_file_date.return_value = ''
        mock_exports.return_value = []

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__empty_self_file_date(self, mock_exports, mock_file_date,
                                       mock_render):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = []

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read, file_date='', exports=EXPORTS_OLD)
        plugin.file_date = ''
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__new_file_date_canonical(self, mock_exports, mock_file_date,
                                          mock_render):
        mock_file_date.return_value = FILE_DATE_NEW
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_NEW)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {'31': TEAM_NEW, '32': TEAM_OLD}
        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        mock_render.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_NEW)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__new_file_date_truncated(self, mock_exports, mock_file_date,
                                          mock_render):
        mock_file_date.return_value = FILE_DATE_NEW
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_TRUNCATED) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_NEW)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {'31': TEAM_NEW_TRUNCATED, '32': TEAM_OLD_TRUNCATED}
        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_not_called()
        mock_render.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_NEW)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__old_file_date(self, mock_exports, mock_file_date,
                                mock_render):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = EXPORTS_NEW

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._run_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_called_once_with(URLOPEN)
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'exports.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_file_date')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_setup(self, mock_exports, mock_file_date, mock_render):
        mock_file_date.return_value = FILE_DATE_OLD
        mock_exports.return_value = EXPORTS_OLD

        read = {k: copy.deepcopy(TEAM_CANONICAL) for k in ['31', '32']}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        mock_file_date.assert_called_once_with(URLOPEN)
        mock_exports.assert_called_once_with(URLOPEN)
        mock_render.assert_called_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.assertEqual(plugin.file_date, FILE_DATE_OLD)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

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

    @mock.patch('plugins.exports.exports_plugin.full_name')
    def test_sorted(self, mock_name):
        mock_name.side_effect = ['Arizona Diamondbacks', 'Atlanta Braves']

        read = {'31': TEAM_NEW_TRUNCATED, '32': TEAM_OLD_TRUNCATED}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)

        actual = plugin._sorted('31')
        expected = [-1, -0.7, -7, -float(1) / 3, 'Arizona Diamondbacks']
        mock_name.assert_called_once_with('31')
        self.assertEqual(actual, expected)

        mock_name.reset_mock()

        actual = plugin._sorted('32')
        expected = [2, -0.6, -6, -0.25, 'Atlanta Braves']
        mock_name.assert_called_once_with('32')
        self.assertEqual(actual, expected)

    @mock.patch.object(ExportsPlugin, '_sorted')
    def test_home(self, mock_sorted):
        mock_sorted.side_effect = [[
            -1, -0.7, -7, -float(1) / 3, 'Arizona Diamondbacks'
        ], [2, -0.6, -6, -0.25, 'Atlanta Braves']]

        read = {'31': TEAM_NEW_TRUNCATED, '32': TEAM_OLD_TRUNCATED}
        plugin = self.create_plugin(
            read, file_date=FILE_DATE_OLD, exports=EXPORTS_OLD)
        ret = plugin._home(date=THEN)
        _table = table(
            cols=['', 'text-center', 'text-center'],
            head=['Team', 'Streak', 'Last 10'],
            body=[['Atlanta Braves', '-2', '6 - 4'],
                  ['Arizona Diamondbacks', '+1', '7 - 3']])
        expected = {'breadcrumbs': BREADCRUMBS, 'table': _table}
        self.assertEqual(ret, expected)


if __name__ in ['__main__', 'plugins.exports.exports_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.exports'
    _pth = 'plugins/exports'
    main(ExportsPluginTest, ExportsPlugin, _pkg, _pth, {}, _main)
