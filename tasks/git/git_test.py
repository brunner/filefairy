#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)


class GitTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_log = mock.patch('tasks.git.git._logger.log')
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

    def create_git(self):
        self.init_mocks({})
        git = Git(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Git._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()
        self.init_mocks({})

        return git

    @mock.patch.object(Git, 'status')
    @mock.patch.object(Git, 'automate')
    def test_notify__with_day(self, mock_automate, mock_status):
        git = self.create_git()
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

        git = self.create_git()
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

        git = self.create_git()
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
        git = self.create_git()
        response = git._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        mock_status.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        git = self.create_git()
        response = git._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_render(self):
        git = self.create_git()
        response = git._render_internal(date=DATE_10260602)
        self.assertEqual(response, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        git = self.create_git()
        response = git._run_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_setup(self):
        git = self.create_git()
        response = git._setup_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_shadow(self):
        git = self.create_git()
        value = git._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

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

        git = self.create_git()
        response = git.add('filefairy', date=DATE_10260602, v=True)
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

        git = self.create_git()
        response = git.automate('filefairy', date=DATE_10260602)
        expected = Response(debug=[adebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=DATE_10260602)
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

        git = self.create_git()
        response = git.automate('filefairy', date=DATE_10260602)
        expected = Response(debug=[cdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=DATE_10260602)
        mock_commit.assert_called_once_with('filefairy', date=DATE_10260602)
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

        git = self.create_git()
        response = git.automate('filefairy', date=DATE_10260602)
        expected = Response(debug=[pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=DATE_10260602)
        mock_commit.assert_called_once_with('filefairy', date=DATE_10260602)
        mock_push.assert_called_once_with('filefairy', date=DATE_10260602)
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

        git = self.create_git()
        response = git.automate('filefairy', date=DATE_10260602)
        expected = Response(
            notify=[Notify.BASE], debug=[adebug, cdebug, pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with('filefairy', date=DATE_10260602)
        mock_commit.assert_called_once_with('filefairy', date=DATE_10260602)
        mock_push.assert_called_once_with('filefairy', date=DATE_10260602)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_commit__with_automated(self):
        stdout = '[master 0abcd0a] Auto...\n1 files\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git()
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

        git = self.create_git()
        response = git.commit('filefairy', date=DATE_10260602, v=True)
        msg = 'Call completed: \'git commit -m "Manual push."\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Manual push.'])
        self.mock_log.assert_not_called()

    def test_pull(self):
        stdout = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'stdout': stdout, 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git()
        response = git.pull('filefairy', date=DATE_10260602, v=True)
        msg = 'Call completed: \'git pull\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_not_called()

    def test_push(self):
        stderr = 'To github.com...\n'
        ret = {'ok': True, 'stdout': '', 'stderr': stderr}
        self.mock_check.return_value = ret

        git = self.create_git()
        response = git.push('filefairy', date=DATE_10260602, v=True)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_not_called()

    def test_reset(self):
        ret = {'ok': True, 'stdout': ''}
        self.mock_check.return_value = ret

        git = self.create_git()
        response = git.reset('filefairy', date=DATE_10260602, v=True)
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

        git = self.create_git()
        response = git.status('filefairy', date=DATE_10260602, v=True)
        msg = 'Call completed: \'git status\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'status'])
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
