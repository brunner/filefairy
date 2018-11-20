#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/exports', '', _path))
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from plugin.exports.exports import Exports  # noqa
from util.component.component import card  # noqa
from util.component.component import cell  # noqa
from util.component.component import col  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from util.team.team import logo_absolute  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

_channel = 'C1234'
_env = env()
_now = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
_now_encoded = '1985-10-26T00:02:30-07:00'
_reactions = {
    'message': {
        'reactions': [{
            'name': 'foo',
            'users': ['U1234', 'U3ULC7DBP']
        }, {
            'name': 'bar',
            'users': ['U5678']
        }]
    },
    'ok': True
}
_then = datetime_datetime_pst(1985, 10, 26, 0, 0, 0)
_then_encoded = '1985-10-26T00:00:00-07:00'
_ts = '123456789'
_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
_urlopen = '<html><head><title>Export Tracker - StatsLab for ...'


def _data(ai=[], channel=_channel, emails=False, form={}, locked=False,
          ts=_ts):
    return {
        'ai': ai,
        'channel': channel,
        'emails': emails,
        'form': form,
        'locked': locked,
        'ts': ts
    }


class ExportsTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_urlopen = mock.patch('plugin.exports.exports.urlopen')
        self.addCleanup(patch_urlopen.stop)
        self.mock_urlopen = patch_urlopen.start()

        patch_chat = mock.patch.object(Exports, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('plugin.exports.exports.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions_add = mock.patch(
            'plugin.exports.exports.reactions_add')
        self.addCleanup(patch_reactions_add.stop)
        self.mock_reactions_add = patch_reactions_add.start()

        patch_reactions_get = mock.patch(
            'plugin.exports.exports.reactions_get')
        self.addCleanup(patch_reactions_get.stop)
        self.mock_reactions_get = patch_reactions_get.start()

        patch_reactions_remove = mock.patch(
            'plugin.exports.exports.reactions_remove')
        self.addCleanup(patch_reactions_remove.stop)
        self.mock_reactions_remove = patch_reactions_remove.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_urlopen.return_value = bytes(_urlopen, 'utf-8')
        self.mock_chat.return_value = {
            'ok': True,
            'channel': _channel,
            'ts': _ts
        }
        self.mock_reactions_get.return_value = _reactions

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_urlopen.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_reactions_add.reset_mock()
        self.mock_reactions_get.reset_mock()
        self.mock_reactions_remove.reset_mock()

    def create_plugin(self, data, exports=None):
        self.init_mocks(data)
        plugin = Exports(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Exports._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if exports:
            plugin.exports = exports

        return plugin

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_unlocked_other(self, mock_lock, mock_render,
                                         mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))
        response = plugin._notify_internal(notify=Notify.OTHER, date=_now)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_unlocked_sim(self, mock_lock, mock_render,
                                       mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))

        form = {k: 'n' for k in ['31', '32', '33']}

        def fake_lock(*args, **kwargs):
            plugin.data['form'] = form
            plugin.data['locked'] = True

        mock_lock.side_effect = fake_lock

        response = plugin._notify_internal(
            notify=Notify.STATSPLUS_SIM, date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(form=form, locked=True)
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(
            notify=Notify.STATSPLUS_SIM, date=_now)
        mock_unlock.assert_not_called()
        self.mock_open.assert_called_once_with(Exports._data(), 'w')
        self.mock_handle.write.assert_called_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_unlocked_file(self, mock_lock, mock_render,
                                        mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))
        response = plugin._notify_internal(
            notify=Notify.LEAGUEFILE_FINISH, date=_now)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_locked_other(self, mock_lock, mock_render,
                                       mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(notify=Notify.OTHER, date=_now)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_locked_sim(self, mock_lock, mock_render,
                                     mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(
            notify=Notify.STATSPLUS_SIM, date=_now)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_locked_file(self, mock_lock, mock_render,
                                      mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        plugin = self.create_plugin(read)

        def fake_unlock(*args, **kwargs):
            plugin.data['locked'] = False

        mock_unlock.side_effect = fake_unlock

        response = plugin._notify_internal(
            notify=Notify.LEAGUEFILE_FINISH, date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(form=form)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(
            notify=Notify.LEAGUEFILE_FINISH, date=_now)
        mock_unlock.assert_called_once_with()
        self.mock_open.assert_called_once_with(Exports._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    def test_on_message(self):
        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_new(self, mock_exports, mock_lock, mock_render):
        new = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        mock_exports.return_value = new

        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(_urlopen)
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, new)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_old(self, mock_exports, mock_lock, mock_render):
        old = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        mock_exports.return_value = old

        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form), exports=old)
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(_urlopen)
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, old)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_ai(self, mock_exports, mock_lock, mock_render):
        new = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        mock_exports.return_value = new

        form = {k: '' for k in ['31', '32', '33']}
        read = _data(ai=['31', '32', '33'], form=form)
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(read, exports=exports)
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        write = _data(ai=['32', '33'], form=form)
        mock_exports.assert_called_once_with(_urlopen)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Exports._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, new)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_empty(self, mock_exports, mock_lock,
                                     mock_render):
        mock_exports.return_value = []

        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(_urlopen)
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_exports')
    @mock.patch.object(Exports, '_emails')
    def test_run__with_exports_emails(self, mock_emails, mock_exports,
                                      mock_render):
        emails = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        mock_exports.return_value = emails

        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)

        def fake_emails(*args, **kwargs):
            plugin.data['emails'] = True

        mock_emails.side_effect = fake_emails

        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.EXPORTS_EMAILS]))

        write = _data(emails=True, form=form)
        mock_exports.assert_called_once_with(_urlopen)
        mock_emails.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Exports._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, emails)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_locked(self, mock_exports, mock_lock, mock_render):
        form = {k: '' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(read, exports=exports)

        response = plugin._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_exports.assert_not_called()
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'table': {}}
        mock_home.return_value = home

        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        value = plugin._render_internal(date=_now)
        index = 'exports/index.html'
        self.assertEqual(value, [(index, '', 'exports.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_exports')
    def test_setup(self, mock_exports, mock_render):
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        mock_exports.return_value = exports

        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))
        response = plugin._setup_internal()
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(_urlopen)
        mock_render.assert_called_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, exports)

    def test_shadow(self):
        form = {k: '' for k in ['31', '32', '33']}
        plugin = self.create_plugin(_data(form=form))
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    def test_exports__with_valid_input(self):
        text = '<td><a href="../teams/team_36.html">Chicago Cubs</a><br><s' + \
               'pan>February 3, 2018<br>New Export</span></td><td><a href=' + \
               '"../teams/team_37.html">Cincinnati Reds</a><br><span>Febru' + \
               'ary 3, 2018<br>Old Export</span></td>'
        actual = Exports._exports(text)
        expected = [('36', 'New'), ('37', 'Old')]
        self.assertEqual(actual, expected)

    def test_exports__with_invalid_input(self):
        text = '<td></td>'
        actual = Exports._exports(text)
        expected = []
        self.assertEqual(actual, expected)

    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__without_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        exports = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                   ('42', 'New'), ('44', 'New')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        response = plugin._home(date=_then)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Exports'
        }]
        cols = [
            col(clazz='position-relative'),
            col(clazz='text-center w-25'),
            col(clazz='text-center w-25')
        ]
        e = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL East'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('33', 'Baltimore', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('34', 'Boston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('35', 'Chicago', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('40', 'Detroit', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('42', 'Houston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        expected = {'breadcrumbs': breadcrumbs, 'standings': [e, c, w]}
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__with_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        exports = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                   ('42', 'Old'), ('44', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        response = plugin._home(date=_then)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Exports'
        }]
        cols = [
            col(clazz='position-relative'),
            col(clazz='text-center w-25'),
            col(clazz='text-center w-25')
        ]
        e = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL East'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('33', 'Baltimore', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('34', 'Boston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('35', 'Chicago', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('40', 'Detroit', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('42', 'Houston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        expected = {'breadcrumbs': breadcrumbs, 'standings': [e, c, w]}
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__with_lock(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        read = _data(form=form, locked=True)
        exports = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                   ('42', 'Old'), ('44', 'Old')]
        plugin = self.create_plugin(read, exports=exports)
        response = plugin._home(date=_then)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Exports'
        }]
        cols = [
            col(clazz='position-relative'),
            col(clazz='text-center w-25'),
            col(clazz='text-center w-25')
        ]
        e = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL East'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('33', 'Baltimore', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('34', 'Boston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('35', 'Chicago', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('40', 'Detroit', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[[
                cell(content=logo_absolute('42', 'Houston', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ], [
                cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                cell(content='1 - 0'),
                cell(content='W1')
            ]])
        expected = {'breadcrumbs': breadcrumbs, 'standings': [e, c, w]}
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_emails(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        read = _data(emails=True, form=form)
        plugin = self.create_plugin(read, exports=exports)
        plugin._lock()

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo', '33': 'onnnonnnon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_truncation(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        plugin._lock()

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo', '33': 'onnnonnnon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Tracker locked.')
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_ai_added(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nooooooooo' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        plugin._lock()

        form = {'31': 'ooooooooon', '32': '', '33': 'ooooooooon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Tracker locked.')
        self.mock_reactions_add.assert_called_once_with('ghost', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data['ai'], ['32'])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_100(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'New'), ('33', 'New')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        plugin._lock()

        form = {k: 'onnnonnnon' for k in ['31', '32', '33']}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Tracker locked.')
        self.mock_reactions_add.assert_called_once_with('100', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_palm_tree(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        plugin._lock()

        form = {k: 'onnnonnnoo' for k in ['31', '32', '33']}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Tracker locked.')
        self.mock_reactions_add.assert_called_once_with(
            'palm_tree', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__without_palm_tree(self, mock_reactions_get):
        mock_reactions_get.return_value = ['palm_tree']

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        plugin = self.create_plugin(_data(form=form), exports=exports)
        plugin._lock()

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo', '33': 'onnnonnnon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Tracker locked.')
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_called_once_with(
            'palm_tree', _channel, _ts)
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, exports)

    def test_new(self):
        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)

        actual = plugin._new()
        expected = (1, 3)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()

    def test_reactions_get(self):
        form = {k: '' for k in ['31', '32', '33']}
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)

        actual = plugin._reactions_get(_channel, _ts)
        expected = ['foo']
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_reactions_remove.assert_not_called()

    def test_streak(self):
        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo'}
        plugin = self.create_plugin(_data(form=form))

        actual = plugin._streak('31')
        expected = 'W1'
        self.assertEqual(actual, expected)
        actual = plugin._streak('32')
        expected = 'L2'
        self.assertEqual(actual, expected)

    @mock.patch('plugin.exports.exports.teamid_to_abbreviation')
    def test_sorted(self, mock_name):
        mock_name.side_effect = ['ARI', 'ATL']

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo'}
        exports = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        plugin = self.create_plugin(_data(form=form), exports=exports)

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
        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        exports = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        plugin = self.create_plugin(read, exports=exports)
        plugin._unlock()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(plugin.exports, exports)
        self.assertFalse(plugin.data['locked'])


if __name__ in ['__main__', 'plugin.exports.exports_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.exports'
    _pth = 'plugin/exports'
    main(ExportsTest, Exports, _pkg, _pth, {}, _main, date=_now, e=_env)
