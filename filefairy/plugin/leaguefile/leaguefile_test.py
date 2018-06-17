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
from core.shadow.shadow import Shadow  # noqa
from core.task.task import Task  # noqa
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
_now = datetime.datetime(2018, 1, 29)
_now_encoded = '2018-01-29T00:00:00'
_server = server()
_then = datetime.datetime(2018, 1, 28)
_then_encoded = '2018-01-28T00:00:00'
_ts = '123456789'
_year = datetime.datetime(2019, 1, 1)
_year_encoded = '2019-01-01T00:00:00'


def _data(completed=[],
          download=None,
          now=_now_encoded,
          then=_then_encoded,
          upload=None):
    return {
        'completed': completed,
        'download': download,
        'now': now,
        'then': then,
        'upload': upload
    }


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
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_valid_input(self, mock_check_download,
                                   mock_check_upload, mock_download,
                                   mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_upload.return_value = iter([check_u, check_c])

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_START]))

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T00:00:00'
        }
        write = _data(upload=upload)
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_with('fairylab', 'Upload started.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Upload started.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_check_false(self, mock_check_download,
                                   mock_check_upload, mock_download,
                                   mock_render):
        mock_check_download.return_value = ('0', '', '', False)
        mock_check_upload.return_value = iter([])
        mock_download.return_value = Response()

        download = {
            'start': 'Jan 29 18:05',
            'size': '20000',
            'end': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(download=download, upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check_download.assert_called_once_with()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_no_filepart_change(self, mock_check_download,
                                          mock_check_upload, mock_download,
                                          mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_upload.return_value = iter([check_u, check_c])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(
            _data(upload=upload, completed=[completed]))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_no_up_change(self, mock_check_download,
                                    mock_check_upload, mock_download,
                                    mock_render):
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])

        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(completed=[completed]))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_check_upload.assert_called_once_with()
        mock_check_download.assert_not_called()
        mock_download.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_empty_filepart_fast(self, mock_check_download,
                                           mock_check_upload, mock_download,
                                           mock_render):
        check = ('328706052', 'Jan 29 15:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check])
        mock_download.return_value = Response()

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        completed = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 15:55',
            'now': '2018-01-29T00:00:00'
        }
        write = _data(upload=completed)
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_called_once_with('zap', _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_empty_filepart_slow(self, mock_check_download,
                                           mock_check_upload, mock_download,
                                           mock_render):
        check = ('328706052', 'Jan 29 07:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check])
        mock_download.return_value = Response()

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        completed = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 07:55',
            'now': '2018-01-29T00:00:00'
        }
        write = _data(upload=completed)
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        timer = 'timer_clock'
        self.mock_reactions.assert_called_once_with(timer, _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_empty_filepart_typical(self, mock_check_download,
                                              mock_check_upload, mock_download,
                                              mock_render):
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])
        mock_download.return_value = Response()

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        completed = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 12:55',
            'now': '2018-01-29T00:00:00'
        }
        write = _data(upload=completed)
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_download_ok_true(self, mock_check_download,
                                        mock_check_upload, mock_download,
                                        mock_render):
        check_d = ('100000', 'Jan 29 18:10',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_download.return_value = check_d
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])
        mock_download.return_value = Response()

        download = {
            'start': 'Jan 29 18:05',
            'size': '20000',
            'end': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(download=download, upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        updated = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 00:00',
            'now': '2018-01-29T00:00:00'
        }
        write = _data(download=updated, upload=upload)
        mock_check_download.assert_called_once_with()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_download_completed(self, mock_check_download,
                                          mock_check_upload, mock_download,
                                          mock_render):
        check_d = ('328706052', 'Jan 29 18:00',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_download.return_value = check_d
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])
        mock_download.return_value = Response()

        download = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 18:10',
            'now': '2018-01-29T00:00:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'date': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(download=download, upload=upload))
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        completed = {
            'size': '328706052',
            'date': 'Jan 29 12:55',
            'ustart': 'Jan 29 16:00',
            'uend': 'Jan 29 18:00',
            'dstart': 'Jan 29 18:05',
            'dend': 'Jan 29 18:10'
        }
        write = _data(completed=[completed])
        mock_check_download.assert_called_once_with()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'upload': {}, 'completed': {}}
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
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_valid_input(self, mock_check, mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_u, check_c])

        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T00:00:00'
        }
        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        write = _data(upload=upload, completed=[completed])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_no_filepart_change(self, mock_check, mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_u, check_c])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(
            _data(upload=upload, completed=[completed]))
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
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_no_up_change(self, mock_check, mock_render):
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_c])

        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(completed=[completed]))
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
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_empty_filepart(self, mock_check, mock_render):
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_c])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(upload=upload))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        completed = {
            'start': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 12:55',
            'date': 'Jan 29 12:55'
        }
        write = _data(completed=[completed])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_new_up(self, mock_check, mock_render):
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check_c])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(
            _data(upload=upload, completed=[completed]))
        response = plugin._setup_internal(date=_now)
        self.assertEqual(response, Response())

        new = {
            'start': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 12:55',
            'date': 'Jan 29 12:55'
        }
        write = _data(completed=[new, completed])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(completed=[completed]))
        value = plugin._shadow_internal()
        self.assertEqual(value, [
            Shadow(
                destination='statsplus',
                key='leaguefile.now',
                data=_now_encoded)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

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
    def test_check_download__with_filepart(self, mock_check, mock_log):
        ls = 'total 60224\n' + \
             '-rw-rw-r-- 1 user user 100000 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check_download()
        expected = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check_download__without_filepart(self, mock_check, mock_log):
        ls = 'total 60224\n' + \
             'drwxrwxr-x 4 user user      4096 Jan 29 00:00 news\n' + \
             '-rw-rw-r-- 1 user user 345678901 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check_download()
        expected = ('345678901', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz', False)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check_download__with_ok_false(self, mock_check, mock_log):
        mock_check.return_value = {'ok': False}

        actual = Leaguefile._check_download()
        expected = ('0', '', '', False)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.logger_.log')
    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check_upload__with_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 ' + \
             'orange_and_blue_league_baseball.tar.gz\n' + \
             '-rwxrwxrwx 1 user user 100000 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz.filepart'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check_upload()
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        expected = iter([check_u, check_c])
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
    def test_check_upload__without_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 328706052 Jan 29 12:55 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'output': ls}

        actual = Leaguefile._check_upload()
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        expected = iter([check_c])
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
    def test_check_upload__with_ok_false(self, mock_check, mock_log):
        mock_check.return_value = {'ok': False, 'output': 'ret'}

        actual = Leaguefile._check_upload()
        expected = iter([])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.ping')
    def test_download__with_ok_false(self, mock_ping):
        mock_ping.return_value = {'ok': False, 'output': 'ret'}

        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(upload=completed))
        response = plugin.download(date=_now)
        self.assertEqual(response, Response())

        self.mock_log.assert_called_once_with(
            logging.WARNING, 'Download failed.', extra={
                'output': 'ret'
            })
        self.assertFalse(plugin.data['download'])

    @mock.patch('plugin.leaguefile.leaguefile.ping')
    def test_download__with_ok_true(self, mock_ping):
        mock_ping.return_value = {'ok': True}

        completed = {
            'start': 'Jan 27 12:00',
            'size': '345678901',
            'end': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(upload=completed))
        response = plugin.download(date=_now)
        self.assertEqual(
            response,
            Response(task=[
                Task(target='_download_internal', kwargs={
                    'date': _now
                })
            ]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')
        self.assertEqual(plugin.data['download'], {
            'start': 'Jan 29 00:00',
            'now': _now_encoded
        })

    @mock.patch.object(Leaguefile, '_leagues')
    @mock.patch('plugin.leaguefile.leaguefile.wget_file')
    @mock.patch('plugin.leaguefile.leaguefile.box_scores')
    def test_download_internal__with_new_year(self, mock_box_scores, mock_file,
                                              mock_leagues):
        mock_box_scores.return_value = _year
        mock_file.return_value = {'ok': True}

        download = {'start': 'Jan 29 18:05', 'now': '2018-01-29T00:00:00'}
        plugin = self.create_plugin(
            _data(download=download, now=_then_encoded))

        response = plugin._download_internal(v=True)
        notify = [Notify.LEAGUEFILE_DOWNLOAD, Notify.LEAGUEFILE_YEAR]
        shadow = plugin._shadow_internal()
        self.assertEqual(response, Response(notify=notify, shadow=shadow))

        write = _data(download=download, now=_year_encoded)
        mock_box_scores.assert_called_once_with(_then)
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')

    @mock.patch.object(Leaguefile, '_leagues')
    @mock.patch('plugin.leaguefile.leaguefile.wget_file')
    @mock.patch('plugin.leaguefile.leaguefile.box_scores')
    def test_download_internal__with_same_year(self, mock_box_scores, mock_file,
                                               mock_leagues):
        mock_box_scores.return_value = _now
        mock_file.return_value = {'ok': True}

        download = {'start': 'Jan 29 18:05', 'now': '2018-01-29T00:00:00'}
        plugin = self.create_plugin(
            _data(download=download, now=_then_encoded))

        response = plugin._download_internal(v=True)
        notify = [Notify.LEAGUEFILE_DOWNLOAD]
        shadow = plugin._shadow_internal()
        self.assertEqual(response, Response(notify=notify, shadow=shadow))

        write = _data(download=download, now=_now_encoded)
        mock_box_scores.assert_called_once_with(_then)
        mock_file.assert_called_once_with()
        mock_leagues.assert_called_once_with()
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')

    @mock.patch.object(Leaguefile, '_leagues')
    @mock.patch('plugin.leaguefile.leaguefile.wget_file')
    @mock.patch('plugin.leaguefile.leaguefile.box_scores')
    def test_download_internal__with_ok_false(self, mock_box_scores, mock_file,
                                              mock_leagues):
        mock_file.return_value = {'ok': False}

        download = {'start': 'Jan 29 18:05', 'now': '2018-01-29T00:00:00'}
        plugin = self.create_plugin(
            _data(download=download, now=_then_encoded))

        response = plugin._download_internal(v=True)
        self.assertEqual(response, Response())

        write = _data(now=_then_encoded)
        mock_box_scores.assert_not_called()
        mock_file.assert_called_once_with()
        mock_leagues.assert_not_called()
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO, 'Download failed.')

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
        cols = [
            '', ' class="text-center"', ' class="text-center"',
            ' class="text-right"'
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=['Date', 'Upload', 'Download', 'Size'],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': None,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_upload(self):
        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(upload=upload))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        upload = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[' class="w-55p"', ''],
                bcols=[' class="w-55p"', ''],
                body=[['Time: ', '2h 0m'], ['Size: ', '100,000']]),
            ts='0s ago',
            success='ongoing')
        cols = [
            '', ' class="text-center"', ' class="text-center"',
            ' class="text-right"'
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=['Date', 'Upload', 'Download', 'Size'],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': upload,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_download(self):
        download = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 18:10',
            'now': '2018-01-29T00:00:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'size': '345678901',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00'
        }
        plugin = self.create_plugin(_data(download=download, upload=upload))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        upload = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[' class="w-55p"', ''],
                bcols=[' class="w-55p"', ''],
                body=[['Time: ', '2h 0m'], ['Size: ', '345,678,901']]),
            ts='0s ago',
            success='completed')
        download = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[' class="w-55p"', ''],
                bcols=[' class="w-55p"', ''],
                body=[['Time: ', '5m'], ['Size: ', '100,000']]),
            ts='0s ago',
            success='ongoing')
        cols = [
            '', ' class="text-center"', ' class="text-center"',
            ' class="text-right"'
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=['Date', 'Upload', 'Download', 'Size'],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': upload,
            'download': download,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_completed(self):
        completed = {
            'size': '345678901',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        plugin = self.create_plugin(_data(completed=[completed]))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        cols = [
            '', ' class="text-center"', ' class="text-center"',
            ' class="text-right"'
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=['Date', 'Upload', 'Download', 'Size'],
            body=[['Jan 27', '0m', '0m', '345,678,901']])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': None,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(Leaguefile, '_leagues_internal')
    @mock.patch('plugin.leaguefile.leaguefile.os.path.isfile')
    def test_leagues(self, mock_isfile, mock_leagues):
        mock_isfile.return_value = True

        plugin = self.create_plugin(_data())
        plugin._leagues()

        leagues = 'resource/download/news/txt/leagues'
        dpath = os.path.join(_root, 'resource/extract/leagues/{}.txt')
        dinjuries = dpath.format('injuries')
        dnews = dpath.format('news')
        dtransactions = dpath.format('transactions')
        fpath = os.path.join(_root, leagues, 'league_100_{}.txt')
        finjuries = fpath.format('injuries')
        fnews = fpath.format('news')
        ftransactions = fpath.format('transactions')
        calls = [
            mock.call(dinjuries),
            mock.call(finjuries),
            mock.call(dnews),
            mock.call(fnews),
            mock.call(dtransactions),
            mock.call(ftransactions),
        ]
        mock_isfile.assert_has_calls(calls)
        calls = [
            mock.call('injuries', dinjuries, finjuries),
            mock.call('news', dnews, fnews),
            mock.call('transactions', dtransactions, ftransactions)
        ]
        mock_leagues.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.open', create=True)
    def test_leagues_internal__injuries(self, mock_open):
        injuries_new = '20180129\t<a href=\"../teams/team_57.html\">Tampa ' + \
                       'Bay Rays</a>: <a href=\"../players/player_1.html\"' + \
                       '>Zack Weiss</a> diagnosed with a strained hamstrin' + \
                       'g, will miss 4 weeks.\n20180129\t<a href=\"../team' + \
                       's/team_39.html\">Colorado Rockies</a>: RF <a href=' + \
                       '\"../players/player_24198.html\">Eddie Hoffman</a>' + \
                       ' was injured being hit by a pitch.  The Diagnosis:' + \
                       ' bruised knee. This is a day-to-day injury expecte' + \
                       'd to last 5 days.'
        injuries_old = '20180126\t<a href=\"../teams/team_44.html\">Los An' + \
                       'geles Angels</a>: CF <a href=\"../players/player_0' + \
                       '.html\">Alex Aristy</a> was injured while running ' + \
                       'the bases.  The Diagnosis: knee inflammation. He\'' + \
                       's expected to miss about 3 weeks.'
        data_a = '\n'.join([injuries_old, injuries_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/injuries.txt'
        fname = 'resource/download/news/txt/leagues/league_100_injuries.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('injuries', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in injuries_new.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.open', create=True)
    def test_leagues_internal__news(self, mock_open):
        news_new = '20180128\t<a href=\"../teams/team_42.html\">Houston As' + \
                   'tros</a>: <a href=\"../players/player_39044.html\">Mar' + \
                   'k Appel</a> pitches a 2-hit shutout against the <a hre' + \
                   'f=\"../teams/team_44.html\">Los Angeles Angels</a> wit' + \
                   'h 8 strikeouts and 0 BB allowed!\n20180129\t<a href=\"' + \
                   '../teams/team_39.html\">Colorado Rockies</a>: <a href=' + \
                   '\"../players/player_30965.html\">Spencer Taylor</a> go' + \
                   't suspended 3 games after ejection following a brawl.'
        news_old = '20180127\t<a href=\"../teams/team_57.html\">Tampa Bay ' + \
                   'Rays</a>: <a href=\"../players/player_27.html\">A.J. R' + \
                   'eed</a> got suspended 4 games after ejection following' + \
                   ' arguing a strike call.'
        data_a = '\n'.join([news_old, news_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/news.txt'
        fname = 'resource/download/news/txt/leagues/league_100_news.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('news', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [mock.call(s + '\n') for s in news_new.split('\n') if s]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _now_encoded)
        self.mock_log.assert_not_called()

    @mock.patch('plugin.leaguefile.leaguefile.open', create=True)
    def test_leagues_internal__transactions(self, mock_open):
        transactions_new = '20180128\t<a href=\"../teams/team_33.html\">Ba' + \
                           'ltimore Orioles</a>: Placed C <a href=\"../pla' + \
                           'yers/player_1439.html\">Evan Skoug</a> on the ' + \
                           'active roster.\n\n20180128\t<a href=\"../teams' + \
                           '/team_33.html\">Baltimore Orioles</a>: Activat' + \
                           'ed C <a href=\"../players/player_1439.html\">E' + \
                           'van Skoug</a> from the disabled list.\n'
        transactions_old = '20180127\t<a href=\"../teams/team_33.html\">Ba' + \
                           'ltimore Orioles</a>: Placed 2B <a href=\"../pl' + \
                           'ayers/player_292.html\">Austin Slater</a> on t' + \
                           'he 7-day disabled list, retroactive to 08/12/2' + \
                           '022.\n'
        data_a = '\n'.join([transactions_old, transactions_new])
        mo_a = mock.mock_open(read_data=data_a)
        mock_handle_a = mo_a()
        mo_b = mock.mock_open()
        mock_handle_b = mo_b()
        mock_open.side_effect = [mo_a.return_value, mo_b.return_value]

        dname = 'resource/extract/transactions.txt'
        fname = 'resource/download/transactions/txt/leagues/' + \
                'league_100_transactions.txt'
        plugin = self.create_plugin(_data(now=_then_encoded))
        plugin._leagues_internal('transactions', dname, fname)

        calls = [
            mock.call(fname, 'r', encoding='iso-8859-1'),
            mock.call(dname, 'w')
        ]
        mock_open.assert_has_calls(calls)
        mock_handle_a.write.assert_not_called()
        calls = [
            mock.call(s + '\n') for s in transactions_new.split('\n') if s
        ]
        mock_handle_b.write.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.assertEqual(plugin.data['now'], _then_encoded)
        self.mock_log.assert_not_called()


if __name__ in ['__main__', 'plugin.leaguefile.leaguefile_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.leaguefile'
    _pth = 'plugin/leaguefile'
    main(LeaguefileTest, Leaguefile, _pkg, _pth, {}, _main, date=_now, e=_env)
