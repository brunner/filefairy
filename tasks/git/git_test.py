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
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from tasks.git.git import Git  # noqa
from types_.debug.debug import Debug  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

FAIRYLAB_DIR = re.sub(r'/filefairy/tasks/git', '', _path) + '/fairylab/static'

ADD_MSG = 'Call completed: \'git add .\'.'
COMMIT_MSG = 'Call completed: \'git commit -m "Automated push."\'.'
PUSH_MSG = 'Call completed: \'git push\'.'


class GitTest(Test):
    def setUp(self):
        check_output_patch = mock.patch('tasks.git.git.check_output')
        self.addCleanup(check_output_patch.stop)
        self.check_output_ = check_output_patch.start()

    def create_git(self):
        git = Git(date=DATE_10260602)

        self.assertNotCalled(self.check_output_)

        return git

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__filefairy_day(self, acp_, chdir_):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.FILEFAIRY_DAY)
        self.assertEqual(response, Response())

        acp_.assert_called_once_with(notify=Notify.FILEFAIRY_DAY)
        self.assertNotCalled(chdir_, self.check_output_)

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__filefairy_deploy(self, acp_, chdir_):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.FILEFAIRY_DEPLOY)
        self.assertEqual(response, Response())

        acp_.assert_called_once_with(notify=Notify.FILEFAIRY_DEPLOY)
        chdir_.assert_called_once_with(FAIRYLAB_DIR)
        self.assertNotCalled(self.check_output_)

    @mock.patch('tasks.git.git.chdir')
    @mock.patch.object(Git, 'acp')
    def test_notify__other(self, acp_, chdir_):
        git = self.create_git()
        response = git._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(acp_, chdir_, self.check_output_)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_add(self, add_, commit_, push_):
        add = Debug(msg=ADD_MSG)
        add_.return_value = Response(debug=[add])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[add])
        self.assertEqual(response, expected)

        add_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(commit_, push_, self.check_output_)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_commit(self, add_, commit_, push_):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)

        add_.return_value = Response(notify=[Notify.BASE], debug=[add])
        commit_.return_value = Response(debug=[commit])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[commit])
        self.assertEqual(response, expected)

        add_.assert_called_once_with(date=DATE_10260602)
        commit_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(push_, self.check_output_)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_failed_push(self, add_, commit_, push_):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)
        push = Debug(msg=PUSH_MSG)

        add_.return_value = Response(notify=[Notify.BASE], debug=[add])
        commit_.return_value = Response(notify=[Notify.BASE], debug=[commit])
        push_.return_value = Response(debug=[push])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(debug=[push])
        self.assertEqual(response, expected)

        add_.assert_called_once_with(date=DATE_10260602)
        commit_.assert_called_once_with(date=DATE_10260602)
        push_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_acp__with_success(self, add_, commit_, push_):
        add = Debug(msg=ADD_MSG)
        commit = Debug(msg=COMMIT_MSG)
        push = Debug(msg=PUSH_MSG)

        add_.return_value = Response(notify=[Notify.BASE], debug=[add])
        commit_.return_value = Response(notify=[Notify.BASE], debug=[commit])
        push_.return_value = Response(notify=[Notify.BASE], debug=[push])

        git = self.create_git()
        response = git.acp(date=DATE_10260602)
        expected = Response(notify=[Notify.BASE], debug=[add, commit, push])
        self.assertEqual(response, expected)

        add_.assert_called_once_with(date=DATE_10260602)
        commit_.assert_called_once_with(date=DATE_10260602)
        push_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_add(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.add(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(['git', 'add', '.'], date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_commit(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.commit(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated push.'], date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_pull(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.pull(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(['git', 'pull'], date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_push(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.push(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(['git', 'push'], date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_reset(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.reset(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(['git', 'reset', '--hard'],
                                       date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    @mock.patch.object(Git, 'check')
    def test_status(self, check_):
        response = Response(debug=[Debug(msg='msg')])
        check_.return_value = response

        git = self.create_git()
        actual = git.status(date=DATE_10260602)
        self.assertEqual(actual, response)

        check_.assert_called_once_with(['git', 'status'], date=DATE_10260602)
        self.assertNotCalled(self.check_output_)

    def test_check__false(self):
        ret = {'ok': False, 'stdout': 'stdout', 'stderr': ''}
        self.check_output_.return_value = ret

        git = self.create_git()
        actual = git.check(['cmd'])
        expected = Response(
            debug=[Debug(msg='Call failed: \'cmd\'.', extra=ret)])
        self.assertEqual(actual, expected)

        self.check_output_.assert_called_once_with(['cmd'])

    def test_check__true(self):
        ret = {'ok': True, 'stdout': 'stdout', 'stderr': ''}
        self.check_output_.return_value = ret

        git = self.create_git()
        actual = git.check(['cmd'])
        expected = Response(
            notify=[Notify.BASE],
            debug=[Debug(msg='Call completed: \'cmd\'.', extra=ret)])
        self.assertEqual(actual, expected)

        self.check_output_.assert_called_once_with(['cmd'])


if __name__ == '__main__':
    unittest.main()
