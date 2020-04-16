#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for git.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/git', '', _path))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from tasks.git.git import Git  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

FAIRYLAB_DIR = re.sub(r'/filefairy/tasks/git', '', _path) + '/fairylab/static'

ADD_MSG = 'Call completed: \'git add .\'.'
COMMIT_MSG = 'Call completed: \'git commit -m "Automated push."\'.'
PUSH_MSG = 'Call completed: \'git push\'.'


class GitTest(Test):
    def setUp(self):
        patch_check = mock.patch('tasks.git.git.check_output')
        self.addCleanup(patch_check.stop)
        self.mock_check = patch_check.start()

    def create_git(self):
        git = Git(date=DATE_10260602, e=ENV)

        self.assertNotCalled(self.mock_check)

        return git

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__filefairy_day(self, mock_acp, mock_chdir):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        mock_acp.assert_called_once_with(notify=Notify.FILEFAIRY_DAY)
        self.assertNotCalled(mock_chdir, self.mock_check)

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__filefairy_deploy(self, mock_acp, mock_chdir):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.FILEFAIRY_DEPLOY)
        self.assertEqual(response, Response())

        mock_acp.assert_called_once_with(notify=Notify.FILEFAIRY_DEPLOY)
        mock_chdir.assert_called_once_with(FAIRYLAB_DIR)
        self.assertNotCalled(self.mock_check)

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__other(self, mock_acp, mock_chdir):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_acp, mock_chdir, self.mock_check)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_add(self, mock_add, mock_commit, mock_push):
        add = Debug(msg=ADD_MSG)
        mock_add.return_value = Response(debug=[add])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[add])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(mock_commit, mock_push, self.mock_check)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_commit(self, mock_add, mock_commit, mock_push):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)

        mock_add.return_value = Response(notify=[Notify.BASE], debug=[add])
        mock_commit.return_value = Response(debug=[commit])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[commit])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=DATE_10260602)
        mock_commit.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(mock_push, self.mock_check)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_push(self, mock_add, mock_commit, mock_push):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)
        push = Debug(msg=PUSH_MSG)

        mock_add.return_value = Response(notify=[Notify.BASE], debug=[add])
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[commit])
        mock_push.return_value = Response(debug=[push])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[push])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=DATE_10260602)
        mock_commit.assert_called_once_with(date=DATE_10260602)
        mock_push.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_success(self, mock_add, mock_commit, mock_push):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)
        push = Debug(msg=PUSH_MSG)

        mock_add.return_value = Response(notify=[Notify.BASE], debug=[add])
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[commit])
        mock_push.return_value = Response(notify=[Notify.BASE], debug=[push])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(notify=[Notify.BASE], debug=[add, commit, push])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=DATE_10260602)
        mock_commit.assert_called_once_with(date=DATE_10260602)
        mock_push.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_add(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.add(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(['git', 'add', '.'],
                                          date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_commit(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.commit(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated push.'], date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_pull(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.pull(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(['git', 'pull'], date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_push(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.push(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(['git', 'push'], date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_reset(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.reset(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(['git', 'reset', '--hard'],
                                          date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    @mock.patch.object(Git, '_call')
    def test_status(self, mock_call):
        response = Response(debug=[Debug(msg='msg')])
        mock_call.return_value = response

        git = self.create_git()
        actual = git.status(date=DATE_10260602)
        self.assertEqual(actual, response)

        mock_call.assert_called_once_with(['git', 'status'],
                                          date=DATE_10260602)
        self.assertNotCalled(self.mock_check)

    def test_call__false(self):
        ret = {'ok': False, 'stdout': 'stdout', 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git()
        actual = git._call(['cmd'])
        expected = Response(
            debug=[Debug(msg='Call failed: \'cmd\'.', extra=ret)])
        self.assertEqual(actual, expected)

        self.mock_check.assert_called_once_with(['cmd'])

    def test_call__true(self):
        ret = {'ok': True, 'stdout': 'stdout', 'stderr': ''}
        self.mock_check.return_value = ret

        git = self.create_git()
        actual = git._call(['cmd'])
        expected = Response(
            notify=[Notify.BASE],
            debug=[Debug(msg='Call completed: \'cmd\'.', extra=ret)])
        self.assertEqual(actual, expected)

        self.mock_check.assert_called_once_with(['cmd'])


if __name__ == '__main__':
    unittest.main()
