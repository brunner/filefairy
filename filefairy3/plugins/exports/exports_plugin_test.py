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
from utils.component.component_util import card, table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import main, TestUtil  # noqa

DATA = ExportsPlugin._data()
EXPORTS_LOCK = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
EXPORTS_OLD = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
EXPORTS_NEW = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
EXPORTS_NEW_HOME = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                    ('42', 'New'), ('44', 'New')]
EXPORTS_OLD_HOME = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                    ('42', 'Old'), ('44', 'Old')]
HOME = {'breadcrumbs': [], 'table': {}}
INDEX = 'html/fairylab/exports/index.html'
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
NOW_ENCODED = '1985-10-26T00:02:30'
FORM_CANONICAL = ''
FORM_TRUNCATED = 'nonnnonnno'
FORM_NEW = 'n'
FORM_NEW_TRUNCATED = 'onnnonnnon'
FORM_OLD = 'o'
FORM_OLD_TRUNCATED = 'onnnonnnoo'
THEN = datetime.datetime(1985, 10, 26, 0, 0, 0)
THEN_ENCODED = '1985-10-26T00:00:00'
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
        patch_chat = mock.patch(
            'plugins.exports.exports_plugin.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_urlopen.return_value = URLOPEN

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_urlopen.reset_mock()
        self.mock_chat.reset_mock()

    def create_plugin(self, data, exports=[], locked=False):
        self.init_mocks(data)
        plugin = ExportsPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.data, data)
        self.assertEqual(plugin.locked, False)

        self.reset_mocks()
        self.init_mocks(data)

        if exports:
            plugin.exports = exports
        if locked:
            plugin.locked = locked

        return plugin

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_unlocked_none(self, mock_lock, mock_render,
                                        mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)
        plugin._notify_internal(activity=ActivityEnum.NONE, date=NOW)

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_unlocked_sim(self, mock_lock, mock_render,
                                       mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)

        form = {k: copy.deepcopy(FORM_NEW) for k in ['31', '32', '33']}

        def fake_lock(*args, **kwargs):
            plugin.locked = True
            plugin.data['form'] = form

        mock_lock.side_effect = fake_lock

        plugin._notify_internal(activity=ActivityEnum.SIM, date=NOW)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form}
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(
            activity=ActivityEnum.SIM, date=NOW)
        mock_unlock.assert_not_called()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_unlocked_file(self, mock_lock, mock_render,
                                        mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)
        plugin._notify_internal(activity=ActivityEnum.FILE, date=NOW)

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_locked_none(self, mock_lock, mock_render,
                                      mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, locked=True)
        plugin._notify_internal(activity=ActivityEnum.NONE, date=NOW)

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_locked_sim(self, mock_lock, mock_render,
                                     mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, locked=True)
        plugin._notify_internal(activity=ActivityEnum.SIM, date=NOW)

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_unlock')
    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    def test_notify__with_locked_file(self, mock_lock, mock_render,
                                      mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, locked=True)

        def fake_unlock(*args, **kwargs):
            plugin.locked = False

        mock_unlock.side_effect = fake_unlock

        plugin._notify_internal(activity=ActivityEnum.FILE, date=NOW)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form}
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_on_message(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)
        ret = plugin._on_message_internal()
        self.assertEqual(ret, ActivityEnum.NONE)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__with_exports_old(self, mock_exports, mock_lock, mock_render):
        mock_exports.return_value = EXPORTS_OLD

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.NONE)

        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__with_exports_new(self, mock_exports, mock_lock, mock_render):
        mock_exports.return_value = EXPORTS_NEW

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.BASE)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form}
        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_lock')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_run__with_exports_lock(self, mock_exports, mock_lock,
                                    mock_render):
        mock_exports.return_value = EXPORTS_LOCK

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW)

        def fake_lock(*args, **kwargs):
            plugin.locked = True

        mock_lock.side_effect = fake_lock

        ret = plugin._run_internal(date=NOW)
        self.assertEqual(ret, ActivityEnum.EXPORT)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form}
        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_LOCK)

    @mock.patch.object(ExportsPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        ret = plugin._render_internal(date=NOW)
        self.assertEqual(ret, [(INDEX, '', 'exports.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(ExportsPlugin, '_render')
    @mock.patch.object(ExportsPlugin, '_exports')
    def test_setup(self, mock_exports, mock_render):
        mock_exports.return_value = EXPORTS_OLD

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)
        plugin._setup_internal()

        mock_exports.assert_called_once_with(URLOPEN)
        mock_render.assert_called_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

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

    maxDiff = None

    @mock.patch.object(ExportsPlugin, '_sorted')
    @mock.patch('plugins.exports.exports_plugin.divisions')
    def test_home__without_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW_HOME)
        ret = plugin._home(date=THEN)
        l = card(
            title='6 / 6',
            table=[{
                'key': 'Rate',
                'value': '100 %'
            }],
            ts='0s ago')
        e = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL East', 'Last 10', 'Streak'],
            body=[['BAL', '1 - 0', 'W1'], ['BOS', '1 - 0', 'W1']])
        c = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL Central', 'Last 10', 'Streak'],
            body=[['CWS', '1 - 0', 'W1'], ['DET', '1 - 0', 'W1']])
        w = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL West', 'Last 10', 'Streak'],
            body=[['HOU', '1 - 0', 'W1'], ['LAA', '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(ret, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_sorted')
    @mock.patch('plugins.exports.exports_plugin.divisions')
    def test_home__with_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD_HOME)
        ret = plugin._home(date=THEN)
        l = card(
            title='4 / 6',
            table=[{
                'key': 'Rate',
                'value': '67 %'
            }, {
                'key': 'Old',
                'value': 'HOU, LAA'
            }],
            ts='0s ago')
        e = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL East', 'Last 10', 'Streak'],
            body=[['BAL', '1 - 0', 'W1'], ['BOS', '1 - 0', 'W1']])
        c = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL Central', 'Last 10', 'Streak'],
            body=[['CWS', '1 - 0', 'W1'], ['DET', '1 - 0', 'W1']])
        w = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL West', 'Last 10', 'Streak'],
            body=[['HOU', '1 - 0', 'W1'], ['LAA', '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(ret, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(ExportsPlugin, '_sorted')
    @mock.patch('plugins.exports.exports_plugin.divisions')
    def test_home__with_lock(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(
            read, exports=EXPORTS_OLD_HOME, locked=True)
        ret = plugin._home(date=THEN)
        l = card(
            title='4 / 6',
            table=[{
                'key': 'Rate',
                'value': '67 %'
            }, {
                'key': 'Old',
                'value': 'HOU, LAA'
            }],
            ts='0s ago')
        e = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL East', 'Last 10', 'Streak'],
            body=[['BAL', '1 - 0', 'W1'], ['BOS', '1 - 0', 'W1']])
        c = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL Central', 'Last 10', 'Streak'],
            body=[['CWS', '1 - 0', 'W1'], ['DET', '1 - 0', 'W1']])
        w = table(
            cols=['', 'text-center w-25', 'text-center w-25'],
            head=['AL West', 'Last 10', 'Streak'],
            body=[['HOU', '1 - 0', 'W1'], ['LAA', '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(ret, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_lock(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin._lock()

        form = {
            '31': FORM_NEW_TRUNCATED,
            '32': FORM_OLD_TRUNCATED,
            '33': FORM_NEW_TRUNCATED
        }
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'testing',
            'Tracker locked and exports recorded.',
            attachments=plugin._attachments())
        self.assertEqual(plugin.data['form'], form)
        self.assertEqual(plugin.exports, EXPORTS_LOCK)
        self.assertEqual(plugin.locked, True)

    def test_old(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW)

        actual = plugin._old()
        expected = 'ATL, BAL'
        self.assertEqual(actual, expected)

    def test_new(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW)

        actual = plugin._new()
        expected = (1, 3)
        self.assertEqual(actual, expected)

    def test_streak(self):
        form = {'31': FORM_NEW_TRUNCATED, '32': FORM_OLD_TRUNCATED}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read)

        actual = plugin._streak('31')
        expected = 'W1'
        self.assertEqual(actual, expected)
        actual = plugin._streak('32')
        expected = 'L2'
        self.assertEqual(actual, expected)

    @mock.patch('plugins.exports.exports_plugin.abbreviation')
    def test_sorted(self, mock_name):
        mock_name.side_effect = ['ARI', 'ATL']

        form = {'31': FORM_NEW_TRUNCATED, '32': FORM_OLD_TRUNCATED}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)

        actual = plugin._sorted('31')
        expected = [-0.7, -7, -1, -float(1) / 3, 'ARI']
        mock_name.assert_called_once_with('31')
        self.assertEqual(actual, expected)

        mock_name.reset_mock()

        actual = plugin._sorted('32')
        expected = [-0.6, -6, 2, -0.25, 'ATL']
        mock_name.assert_called_once_with('32')
        self.assertEqual(actual, expected)

    def test_unlock(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK, locked=True)
        plugin._unlock()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_LOCK)
        self.assertEqual(plugin.locked, False)


if __name__ in ['__main__', 'plugins.exports.exports_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.exports'
    _pth = 'plugins/exports'
    main(ExportsPluginTest, ExportsPlugin, _pkg, _pth, {}, _main)
