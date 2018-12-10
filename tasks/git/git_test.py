#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/git', '', _path))
from data.debug.debug import Debug  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.git.git import Git  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

_commit = 'https://github.com/brunner/filefairy/commit/'
_env = env()
_l = ['d-inline-block', 'w-65p']
_now = datetime_datetime_pst(1985, 10, 27, 0, 0, 0)
_now_encoded = '1985-10-27T00:00:00-07:00'
_r = ['d-inline-block', 'text-right', 'w-65p']
_then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)


def _data(pull=None, push=None):
    if pull is None:
        pull = []
    if push is None:
        push = []
    return {'pull': pull, 'push': push}


class GitTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_log = mock.patch('tasks.git.git.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_check = mock.patch('tasks.git.git.check_output')
        self.addCleanup(patch_check.stop)
        self.mock_check = patch_check.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_log.reset_mock()
        self.mock_check.reset_mock()

    def create_git(self, data):
        self.init_mocks(data)
        git = Git(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Git._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return git

    @mock.patch.object(Git, 'status')
    @mock.patch.object(Git, 'automate')
    def test_notify__with_day(self, mock_automate, mock_status):
        git = self.create_git(_data())
        response = git._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        mock_automate.assert_called_once_with(
            'filefairy', notify=Notify.FILEFAIRY_DAY)
        mock_status.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'status')
    @mock.patch.object(Git, 'automate')
    def test_notify__with_deploy_false(self, mock_automate, mock_status):
        debug = Debug(
            msg='Call completed: \'git status\'.',
            extra={'stdout': 'nothing to commit'})
        mock_status.return_value = Response(
            notify=[Notify.BASE], debug=[debug])

        git = self.create_git(_data())
        response = git._notify_internal(notify=Notify.FILEFAIRY_DEPLOY)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        mock_status.assert_called_once_with(
            'fairylab', notify=Notify.FILEFAIRY_DEPLOY)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'status')
    @mock.patch.object(Git, 'automate')
    def test_run__with_deploy_true(self, mock_automate, mock_status):
        debug = Debug(
            msg='Call completed: \'git status\'.',
            extra={'stdout': 'Changes not staged for commit'})
        mock_status.return_value = Response(
            notify=[Notify.BASE], debug=[debug])

        git = self.create_git(_data())
        response = git._notify_internal(notify=Notify.FILEFAIRY_DEPLOY)
        self.assertEqual(response, Response())

        mock_automate.assert_called_once_with(
            'fairylab', notify=Notify.FILEFAIRY_DEPLOY)
        mock_status.assert_called_once_with(
            'fairylab', notify=Notify.FILEFAIRY_DEPLOY)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'status')
    @mock.patch.object(Git, 'automate')
    def test_notify__with_other(self, mock_automate, mock_status):
        git = self.create_git(_data())
        response = git._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        mock_status.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        git = self.create_git(_data())
        response = git._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'pull': [], 'push': []}
        mock_home.return_value = home

        git = self.create_git(_data())
        response = git._render_internal(date=_now)
        index = 'git/index.html'
        self.assertEqual(response, [(index, '', 'git.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        git = self.create_git(_data())
        response = git._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, '_render')
    def test_setup(self, mock_render):
        git = self.create_git(_data())
        response = git._setup_internal(date=_then)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_shadow(self):
        git = self.create_git(_data())
        value = git._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_firstlast__with_gitlog(self):
        stdout = '"abcdefghijklm"\n"nopqrstuvwxyz"'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        text = 'To github.com:brunner/filefairy.git\n  abcdefgh.' + \
               '.nopqrstu  master -> master'
        first, last = Git._firstlast(text)
        self.assertEqual(first, 'abcdefghijklm')
        self.assertEqual(last, 'nopqrstuvwxyz')

        self.mock_check.assert_called_once_with(
            ['git', 'log', '-20', '--format="%H"'])
        self.mock_log.assert_not_called()

    def test_firstlast__with_match(self):
        ret = {'ok': True, 'stdout': '', 'stderr': ''}
        self.mock_check.return_value = ret

        text = 'To github.com:brunner/filefairy.git\n  abcdefgh.' + \
               '.nopqrstu  master -> master'
        first, last = Git._firstlast(text)
        self.assertEqual(first, 'abcdefgh')
        self.assertEqual(last, 'nopqrstu')

        self.mock_check.assert_called_once_with(
            ['git', 'log', '-20', '--format="%H"'])
        self.mock_log.assert_not_called()

    def test_firstlast__without_match(self):
        first, last = Git._firstlast('')
        self.assertEqual(first, '???????')
        self.assertEqual(last, '???????')

        self.mock_check.assert_not_called()
        self.mock_log.assert_not_called()

    def test_call__with_ok_false(self):
        stdout = 'ret'
        ret = {'ok': False, 'stdout': stdout}
        self.mock_check.return_value = ret

        response = Git._call(['cmd'], 'filefairy', **{})
        msg = 'Call failed: \'cmd\'.'
        expected = Response(debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_call__with_ok_true(self):
        stdout = 'ret'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        response = Git._call(['cmd'], 'filefairy', **{})
        msg = 'Call completed: \'cmd\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_add(self):
        stdout = 'ret'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.add('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git add .\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'add', '.'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_failed_add(self, mock_add, mock_commit, mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(debug=[adebug])

        git = self.create_git(_data())
        response = git.automate('filefairy', date=_now)
        expected = Response(debug=[adebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=_now)
        mock_commit.assert_not_called()
        mock_push.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_failed_commit(self, mock_add, mock_commit,
                                          mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(notify=[Notify.BASE], debug=[adebug])
        cdebug = Debug(
            msg='Call completed: \'git commit -m "Automated push."\'.')
        mock_commit.return_value = Response(debug=[cdebug])

        git = self.create_git(_data())
        response = git.automate('filefairy', date=_now)
        expected = Response(debug=[cdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=_now)
        mock_commit.assert_called_once_with('filefairy', date=_now)
        mock_push.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_failed_push(self, mock_add, mock_commit,
                                        mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(notify=[Notify.BASE], debug=[adebug])
        cdebug = Debug(
            msg='Call completed: \'git commit -m "Automated push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(debug=[pdebug])

        git = self.create_git(_data())
        response = git.automate('filefairy', date=_now)
        expected = Response(debug=[pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=_now)
        mock_commit.assert_called_once_with('filefairy', date=_now)
        mock_push.assert_called_once_with('filefairy', date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_success(self, mock_add, mock_commit, mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(notify=[Notify.BASE], debug=[adebug])
        cdebug = Debug(
            msg='Call completed: \'git commit -m "Automated push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(notify=[Notify.BASE], debug=[pdebug])

        git = self.create_git(_data())
        response = git.automate('filefairy', date=_now)
        expected = Response(
            notify=[Notify.BASE], debug=[adebug, cdebug, pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=_now)
        mock_commit.assert_called_once_with('filefairy', date=_now)
        mock_push.assert_called_once_with('filefairy', date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_commit__with_automated(self):
        stdout = '[master 0abcd0a] Auto...\n1 files\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.commit('filefairy')
        msg = 'Call completed: \'git commit -m "Automated push."\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated push.'])
        self.mock_log.assert_not_called()

    def test_commit__with_manual(self):
        stdout = '[master 0abcd0a] Auto...\n1 files\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.commit('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git commit -m "Manual push."\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Manual push.'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_save')
    def test_pull__with_fairylab(self, mock_save):
        stdout = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.pull('fairylab', date=_now, v=True)
        msg = 'Call completed: \'git pull\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_save')
    def test_pull__with_filefairy(self, mock_save):
        stdout = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.pull('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git pull\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_called_once_with(
            response, 'pull', Git._stdout, date=_now, v=True)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Fetched latest changes.')

    @mock.patch.object(Git, '_save')
    def test_push__with_fairylab_automated(self, mock_save):
        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.push('fairylab', date=_now)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_save')
    def test_push__with_fairylab_manual(self, mock_save):
        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.push('fairylab', date=_now, v=True)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_save')
    def test_push__with_filefairy_automated(self, mock_save):
        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.push('filefairy', date=_now)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_called_once_with(
            response, 'push', Git._stderr, date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(logging.INFO, 'Automated push.')

    @mock.patch.object(Git, '_save')
    def test_push__with_filefairy_manual(self, mock_save):
        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.push('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_called_once_with(
            response, 'push', Git._stderr, date=_now, v=True)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(logging.INFO, 'Manual push.')

    def test_reset(self):
        ret = {'ok': True, 'stdout': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.reset('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git reset --hard\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        self.mock_log.assert_not_called()

    def test_status(self):
        stdout = 'On branch master\nYour branch...\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git(_data())
        response = git.status('filefairy', date=_now, v=True)
        msg = 'Call completed: \'git status\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'status'])
        self.mock_log.assert_not_called()

    def test_home__with_empty(self):
        git = self.create_git(_data())
        actual = git._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Git'
        }]
        expected = {'breadcrumbs': breadcrumbs}
        self.assertEqual(actual, expected)

    def test_home__with_pull(self):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        git = self.create_git(
            _data(pull=[{
                'date': _now_encoded,
                'first': first,
                'last': last
            }]))
        actual = git._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Git'
        }]
        ffirst = span(_l, anchor(_commit + 'abcdefghijklm', 'abcdefg'))
        flast = span(_r, anchor(_commit + 'nopqrstuvwxyz', 'nopqrst'))
        pull = table(
            clazz='border mt-3',
            head=[cell(content='Range')],
            hcols=[col(colspan='2')],
            bcols=[col(), col(clazz='text-right')],
            body=[[
                cell(content=(ffirst + ' ... ' + flast)),
                cell(content='Oct 27 00:00')
            ]])
        expected = {'breadcrumbs': breadcrumbs, 'pull': pull}
        self.assertEqual(actual, expected)

    def test_home__with_push(self):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        git = self.create_git(
            _data(push=[{
                'date': _now_encoded,
                'first': first,
                'last': last
            }]))
        actual = git._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Git'
        }]
        ffirst = span(_l, anchor(_commit + 'abcdefghijklm', 'abcdefg'))
        flast = span(_r, anchor(_commit + 'nopqrstuvwxyz', 'nopqrst'))
        push = table(
            clazz='border mt-3',
            head=[cell(content='Range')],
            hcols=[col(colspan='2')],
            bcols=[col(), col(clazz='text-right')],
            body=[[
                cell(content=(ffirst + ' ... ' + flast)),
                cell(content='Oct 27 00:00')
            ]])
        expected = {'breadcrumbs': breadcrumbs, 'push': push}
        self.assertEqual(actual, expected)

    @mock.patch.object(Git, '_render')
    @mock.patch.object(Git, '_firstlast')
    def test_save__with_pull(self, mock_firstlast, mock_render):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        mock_firstlast.return_value = (first, last)

        stdout = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        msg = 'Call completed: \'git pull\'.'
        response = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])

        git = self.create_git(_data())
        git._save(response, 'pull', Git._stdout, date=_now, v=True)

        write = _data(pull=[{
            'date': _now_encoded,
            'first': first,
            'last': last
        }])
        mock_firstlast.assert_called_once_with(stdout)
        mock_render.assert_called_once_with(date=_now, v=True)
        self.mock_open.assert_called_once_with(Git._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_check.assert_not_called()
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_render')
    @mock.patch.object(Git, '_firstlast')
    def test_save__with_push(self, mock_firstlast, mock_render):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        mock_firstlast.return_value = (first, last)

        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        msg = 'Call completed: \'git pull\'.'
        response = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])

        git = self.create_git(_data())
        git._save(response, 'push', Git._stderr, date=_now, v=True)

        write = _data(push=[{
            'date': _now_encoded,
            'first': first,
            'last': last
        }])
        mock_firstlast.assert_called_once_with(stderr)
        mock_render.assert_called_once_with(date=_now, v=True)
        self.mock_open.assert_called_once_with(Git._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_check.assert_not_called()
        self.mock_log.assert_not_called()


if __name__ in ['__main__', 'tasks.git.git_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.git'
    _pth = 'tasks/git'
    main(GitTest, Git, _pkg, _pth, {}, _main, date=_now, e=_env)