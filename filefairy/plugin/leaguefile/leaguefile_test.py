#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/leaguefile', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.leaguefile.leaguefile import Leaguefile  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.secrets.secrets import server  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_channel = 'C1234'
_env = env()
_now = datetime.datetime(2018, 1, 29, 15, 1, 30)
_server = server()
_ts = '123456789'

def _data(fp=None, up=[]):
    return {'fp': fp, 'up': up}


class LeaguefileTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Leaguefile, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('plugin.leaguefile.leaguefile.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions = mock.patch(
            'plugin.leaguefile.leaguefile.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_chat.return_value = {
            'ok': True,
            'channel': _channel,
            'ts': _ts
        }

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Leaguefile(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Leaguefile._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify(self):
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_valid_input(self, mock_check, mock_render):
        check_fp = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_fp, check_up])

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_START]))

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T15:01:30'
        }
        write = _data(fp=fp)
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_with('fairylab', 'Upload started.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Upload started.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_no_filepart_change(self, mock_check, mock_render):
        check_fp = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_fp, check_up])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(fp=fp, up=[up]))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_no_up_change(self, mock_check, mock_render):
        check_up = ('328706052', 'Jan 29 12:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_up])

        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(up=[up]))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_fast(self, mock_check, mock_render):
        check = ('328706052', 'Jan 29 15:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        plugin = self.create_plugin(_data(fp=fp))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        up = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 15:55'
        }
        write = _data(up=[up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_called_once_with('zap', _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_slow(self, mock_check, mock_render):
        check = ('328706052', 'Jan 29 07:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        plugin = self.create_plugin(_data(fp=fp))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        up = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 07:55'
        }
        write = _data(up=[up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        timer = 'timer_clock'
        self.mock_reactions.assert_called_once_with(timer, _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_typical(self, mock_check, mock_render):
        check_up = ('328706052', 'Jan 29 12:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_up])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        plugin = self.create_plugin(_data(fp=fp))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        up = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 12:55'
        }
        write = _data(up=[up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'fp': {}, 'up': {}}
        mock_home.return_value = home

        plugin = self.create_plugin(_data())
        response = plugin._render_internal(date=_now)
        index = 'html/fairylab/leaguefile/index.html'
        self.assertEqual(response, [(index, '', 'leaguefile.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_valid_input(self, mock_check, mock_render):
        check_fp = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_fp, check_up])

        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T15:01:30'
        }
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        write = _data(fp=fp, up=[up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_no_filepart_change(self, mock_check, mock_render):
        check_fp = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_fp, check_up])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(fp=fp, up=[up]))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_no_up_change(self, mock_check, mock_render):
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_up])

        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(up=[up]))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_empty_filepart(self, mock_check, mock_render):
        check_up = ('328706052', 'Jan 29 12:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_up])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        plugin = self.create_plugin(_data(fp=fp))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        up = {
            'start': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 12:55',
            'date': 'Jan 29 12:55'
        }
        write = _data(up=[up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_new_up(self, mock_check, mock_render):
        check_up = ('328706052', 'Jan 29 12:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_up])

        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(fp=fp, up=[up]))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        new = {
            'start': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 12:55',
            'date': 'Jan 29 12:55'
        }
        write = _data(up=[new, up])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(up=[up]))
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_filedate(self):
        s = 'Jan 29 15:55'
        actual = Leaguefile._filedate(s)
        expected = 'Jan 29'
        self.assertEqual(actual, expected)

    def test_size(self):
        s = '328706052'
        actual = Leaguefile._size(s)
        expected = '328,706,052'
        self.assertEqual(actual, expected)

    def test_time(self):
        s = 'Jan 29 14:00'
        e = 'Jan 29 16:00'
        actual = Leaguefile._time(s, e)
        expected = '2h 0m'
        self.assertEqual(actual, expected)

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check__with_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 ' + \
             'orange_and_blue_league_baseball.tar.gz\n' + \
             '-rwxrwxrwx 1 user user 100000 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz.filepart'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check()
        check_fp = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_up = ('345678901', 'Jan 27 12:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        expected = iter([check_fp, check_up])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check__without_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 328706052 Jan 29 12:55 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check()
        check_up = ('328706052', 'Jan 29 12:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
        expected = iter([check_up])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check__with_ok_false(self, mock_check, mock_log):
        mock_check.return_value = {'ok': False, 'output': 'ret'}

        actual = Leaguefile._check()
        expected = iter([])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    def test_home__with_empty(self):
        plugin = self.create_plugin(_data())
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        up = table(head=['Date', 'Time', 'Size'], body=[])
        expected = {'breadcrumbs': breadcrumbs, 'fp': None, 'up': up}
        self.assertEqual(actual, expected)

    def test_home__with_filepart(self):
        fp = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T15:01:30'
        }
        plugin = self.create_plugin(_data(fp=fp))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        fp = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[' class="w-55p"', ''],
                bcols=[' class="w-55p"', ''],
                body=[['Time: ', '2h 0m'], ['Size: ', '100,000']]),
            ts='0s ago',
            success='ongoing')
        up = table(head=['Date', 'Time', 'Size'], body=[])
        expected = {'breadcrumbs': breadcrumbs, 'fp': fp, 'up': up}
        self.assertEqual(actual, expected)

    def test_home__with_up(self):
        up = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(up=[up]))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        up = table(
            head=['Date', 'Time', 'Size'],
            body=[['Jan 27', '0m', '345,678,901']])
        expected = {'breadcrumbs': breadcrumbs, 'fp': None, 'up': up}
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'plugin.leaguefile.leaguefile_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.leaguefile'
    _pth = 'plugin/leaguefile'
    main(LeaguefileTest, Leaguefile, _pkg, _pth, {}, _main, date=_now, e=_env)
