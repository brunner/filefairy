#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/exports', '', _path))
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.exports.exports import Exports  # noqa
from util.team.team import logo_absolute  # noqa

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

        patch_urlopen = mock.patch('tasks.exports.exports.urlopen')
        self.addCleanup(patch_urlopen.stop)
        self.mock_urlopen = patch_urlopen.start()

        patch_chat = mock.patch.object(Exports, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('tasks.exports.exports.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions_add = mock.patch('tasks.exports.exports.reactions_add')
        self.addCleanup(patch_reactions_add.stop)
        self.mock_reactions_add = patch_reactions_add.start()

        patch_reactions_get = mock.patch('tasks.exports.exports.reactions_get')
        self.addCleanup(patch_reactions_get.stop)
        self.mock_reactions_get = patch_reactions_get.start()

        patch_reactions_remove = mock.patch(
            'tasks.exports.exports.reactions_remove')
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

    def create_exports(self, data, teams=None):
        self.init_mocks(data)
        exports = Exports(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Exports._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if teams:
            exports.teams = teams

        return exports

    @mock.patch.object(Exports, '_unlock')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    def test_notify__with_unlocked_other(self, mock_lock, mock_render,
                                         mock_unlock):
        form = {k: '' for k in ['31', '32', '33']}
        exports = self.create_exports(_data(form=form))
        response = exports._notify_internal(notify=Notify.OTHER, date=_now)
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
        exports = self.create_exports(_data(form=form))

        form = {k: 'n' for k in ['31', '32', '33']}

        def fake_lock(*args, **kwargs):
            exports.data['form'] = form
            exports.data['locked'] = True

        mock_lock.side_effect = fake_lock

        response = exports._notify_internal(
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
        exports = self.create_exports(_data(form=form))
        response = exports._notify_internal(
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
        exports = self.create_exports(read)
        response = exports._notify_internal(notify=Notify.OTHER, date=_now)
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
        exports = self.create_exports(read)
        response = exports._notify_internal(
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
        exports = self.create_exports(read)

        def fake_unlock(*args, **kwargs):
            exports.data['locked'] = False

        mock_unlock.side_effect = fake_unlock

        response = exports._notify_internal(
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
        exports = self.create_exports(_data(form=form))
        response = exports._on_message_internal()
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
    @mock.patch.object(Exports, '_teams')
    def test_run__with_exports_new(self, mock_teams, mock_lock, mock_render):
        new = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        mock_teams.return_value = new

        form = {k: '' for k in ['31', '32', '33']}
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)
        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_teams.assert_called_once_with(_urlopen)
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
        self.assertEqual(exports.teams, new)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_teams')
    def test_run__with_exports_old(self, mock_teams, mock_lock, mock_render):
        old = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        mock_teams.return_value = old

        form = {k: '' for k in ['31', '32', '33']}
        exports = self.create_exports(_data(form=form), teams=old)
        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_teams.assert_called_once_with(_urlopen)
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
        self.assertEqual(exports.teams, old)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_teams')
    def test_run__with_exports_ai(self, mock_teams, mock_lock, mock_render):
        new = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        mock_teams.return_value = new

        form = {k: '' for k in ['31', '32', '33']}
        read = _data(ai=['31', '32', '33'], form=form)
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(read, teams=teams)
        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response())

        write = _data(ai=['32', '33'], form=form)
        mock_teams.assert_called_once_with(_urlopen)
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
        self.assertEqual(exports.teams, new)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_teams')
    def test_run__with_exports_empty(self, mock_teams, mock_lock, mock_render):
        mock_teams.return_value = []

        form = {k: '' for k in ['31', '32', '33']}
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)
        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_teams.assert_called_once_with(_urlopen)
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
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_teams')
    @mock.patch.object(Exports, '_emails')
    def test_run__with_exports_emails(self, mock_emails, mock_teams,
                                      mock_render):
        emails = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        mock_teams.return_value = emails

        form = {k: '' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)

        def fake_emails(*args, **kwargs):
            exports.data['emails'] = True

        mock_emails.side_effect = fake_emails

        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.EXPORTS_EMAILS]))

        write = _data(emails=True, form=form)
        mock_teams.assert_called_once_with(_urlopen)
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
        self.assertEqual(exports.teams, emails)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock')
    @mock.patch.object(Exports, '_teams')
    def test_run__with_locked(self, mock_teams, mock_lock, mock_render):
        form = {k: '' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(read, teams=teams)

        response = exports._run_internal(date=_now)
        self.assertEqual(response, Response())

        mock_teams.assert_not_called()
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
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'table': {}}
        mock_home.return_value = home

        form = {k: '' for k in ['31', '32', '33']}
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)
        value = exports._render_internal(date=_now)
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
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_teams')
    def test_setup(self, mock_teams, mock_render):
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        mock_teams.return_value = teams

        form = {k: '' for k in ['31', '32', '33']}
        exports = self.create_exports(_data(form=form))
        response = exports._setup_internal()
        self.assertEqual(response, Response())

        mock_teams.assert_called_once_with(_urlopen)
        mock_render.assert_called_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(_url)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.teams, teams)

    def test_shadow(self):
        form = {k: '' for k in ['31', '32', '33']}
        exports = self.create_exports(_data(form=form))
        value = exports._shadow_internal()
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
        actual = Exports._teams(text)
        expected = [('36', 'New'), ('37', 'Old')]
        self.assertEqual(actual, expected)

    def test_exports__with_invalid_input(self):
        text = '<td></td>'
        actual = Exports._teams(text)
        expected = []
        self.assertEqual(actual, expected)

    @mock.patch.object(Exports, '_sorted')
    @mock.patch('tasks.exports.exports.divisions')
    def test_home__without_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        teams = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                 ('42', 'New'), ('44', 'New')]
        exports = self.create_exports(_data(form=form), teams=teams)
        response = exports._home(date=_then)
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
            body=[
                [
                    cell(content=logo_absolute('33', 'Baltimore', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('34', 'Boston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('35', 'Chicago', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('40', 'Detroit', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('42', 'Houston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
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
    @mock.patch('tasks.exports.exports.divisions')
    def test_home__with_old(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        teams = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                 ('42', 'Old'), ('44', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)
        response = exports._home(date=_then)
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
            body=[
                [
                    cell(content=logo_absolute('33', 'Baltimore', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('34', 'Boston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('35', 'Chicago', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('40', 'Detroit', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('42', 'Houston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
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
    @mock.patch('tasks.exports.exports.divisions')
    def test_home__with_lock(self, mock_divisions, mock_sorted):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: 'n' for k in keys}
        read = _data(form=form, locked=True)
        teams = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                 ('42', 'Old'), ('44', 'Old')]
        exports = self.create_exports(read, teams=teams)
        response = exports._home(date=_then)
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
            body=[
                [
                    cell(content=logo_absolute('33', 'Baltimore', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('34', 'Boston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        c = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL Central'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('35', 'Chicago', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('40', 'Detroit', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
        w = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='AL West'),
                cell(content='Last 10'),
                cell(content='Streak')
            ],
            body=[
                [
                    cell(content=logo_absolute('42', 'Houston', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
                [
                    cell(content=logo_absolute('44', 'Los Angeles', 'left')),
                    cell(content='1 - 0'),
                    cell(content='W1')
                ],
            ])
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
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        read = _data(emails=True, form=form)
        exports = self.create_exports(read, teams=teams)
        exports._lock()

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
        self.assertEqual(exports.data['ai'], [])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_truncation(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        exports = self.create_exports(_data(form=form), teams=teams)
        exports._lock()

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo', '33': 'onnnonnnon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.data['ai'], [])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_ai_added(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nooooooooo' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        exports = self.create_exports(_data(form=form), teams=teams)
        exports._lock()

        form = {'31': 'ooooooooon', '32': '', '33': 'ooooooooon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_called_once_with('ghost', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.data['ai'], ['32'])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_100(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'New'), ('33', 'New')]
        exports = self.create_exports(_data(form=form), teams=teams)
        exports._lock()

        form = {k: 'onnnonnnon' for k in ['31', '32', '33']}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_called_once_with('100', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.data['ai'], [])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__with_palm_tree(self, mock_reactions_get):
        mock_reactions_get.return_value = []

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)
        exports._lock()

        form = {k: 'onnnonnnoo' for k in ['31', '32', '33']}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_called_once_with(
            'palm_tree', _channel, _ts)
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.data['ai'], [])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    @mock.patch.object(Exports, '_reactions_get')
    def test_lock__without_palm_tree(self, mock_reactions_get):
        mock_reactions_get.return_value = ['palm_tree']

        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        exports = self.create_exports(_data(form=form), teams=teams)
        exports._lock()

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo', '33': 'onnnonnnon'}
        mock_reactions_get.assert_called_once_with(_channel, _ts)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_called_once_with(
            'palm_tree', _channel, _ts)
        self.assertEqual(exports.data['ai'], [])
        self.assertEqual(exports.data['form'], form)
        self.assertTrue(exports.data['locked'], True)
        self.assertEqual(exports.teams, teams)

    def test_new(self):
        form = {k: '' for k in ['31', '32', '33']}
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)

        actual = exports._new()
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
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)

        actual = exports._reactions_get(_channel, _ts)
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
        exports = self.create_exports(_data(form=form))

        actual = exports._streak('31')
        expected = 'W1'
        self.assertEqual(actual, expected)
        actual = exports._streak('32')
        expected = 'L2'
        self.assertEqual(actual, expected)

    @mock.patch('tasks.exports.exports.teamid_to_abbreviation')
    def test_sorted(self, mock_name):
        mock_name.side_effect = ['ARI', 'ATL']

        form = {'31': 'onnnonnnon', '32': 'onnnonnnoo'}
        teams = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
        exports = self.create_exports(_data(form=form), teams=teams)

        actual = exports._sorted('31')
        expected = [-0.7, -7, -1, -float(1) / 3, 'ARI']
        mock_name.assert_called_once_with('31')
        self.assertEqual(actual, expected)

        mock_name.reset_mock()

        actual = exports._sorted('32')
        expected = [-0.6, -6, 2, -0.25, 'ATL']
        mock_name.assert_called_once_with('32')
        self.assertEqual(actual, expected)

    def test_unlock(self):
        form = {k: 'nonnnonnno' for k in ['31', '32', '33']}
        read = _data(form=form, locked=True)
        teams = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
        exports = self.create_exports(read, teams=teams)
        exports._unlock()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions_add.assert_not_called()
        self.mock_reactions_get.assert_not_called()
        self.mock_reactions_remove.assert_not_called()
        self.assertEqual(exports.teams, teams)
        self.assertFalse(exports.data['locked'])


if __name__ in ['__main__', 'tasks.exports.exports_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.exports'
    _pth = 'tasks/exports'
    main(ExportsTest, Exports, _pkg, _pth, {}, _main, date=_now, e=_env)
