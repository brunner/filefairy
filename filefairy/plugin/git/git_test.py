#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/git', '', _path))
from core.debug.debug import Debug  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.git.git import Git  # noqa

_now = datetime.datetime(1985, 10, 27, 0, 0, 0)
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)


class GitTest(unittest.TestCase):
    def setUp(self):
        patch_log = mock.patch('plugin.git.git.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_check = mock.patch('plugin.git.git.check_output')
        self.addCleanup(patch_check.stop)
        self.mock_check = patch_check.start()

    def reset_mocks(self):
        self.mock_log.reset_mock()
        self.mock_check.reset_mock()

    def create_plugin(self, day=0):
        plugin = Git(date=_now)

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()

        return plugin

    @mock.patch.object(Git, 'automate')
    def test_notify__with_day(self, mock_automate):
        plugin = self.create_plugin()
        response = plugin._notify_internal(notify=Notify.FAIRYLAB_DAY)
        self.assertEqual(response, Response())

        mock_automate.assert_called_once_with(notify=Notify.FAIRYLAB_DAY)
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'automate')
    def test_notify__with_other(self, mock_automate):
        plugin = self.create_plugin()
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin()
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin()
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_setup(self):
        plugin = self.create_plugin()
        response = plugin._setup_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin()
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_call__with_ok_false(self):
        output = 'ret'
        self.mock_check.return_value = {'ok': False, 'output': output}

        plugin = self.create_plugin()
        response = plugin._call(['cmd'], **{})
        msg = 'Call failed: \'cmd\'.'
        extra = {'output': output}
        expected = Response(debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_call__with_ok_true(self):
        output = 'ret'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin._call(['cmd'], **{})
        msg = 'Call completed: \'cmd\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_add(self):
        output = 'ret'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin.add(v=True)
        msg = 'Call completed: \'git add .\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['git', 'add', '.'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_failed_add(self, mock_add, mock_commit, mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(debug=[adebug])

        plugin = self.create_plugin()
        response = plugin.automate(date=_now)
        expected = Response(debug=[adebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_not_called()
        mock_push.assert_not_called()
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
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(debug=[cdebug])

        plugin = self.create_plugin()
        response = plugin.automate(date=_now)
        expected = Response(debug=[cdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
        mock_push.assert_not_called()
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
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(debug=[pdebug])

        plugin = self.create_plugin()
        response = plugin.automate(date=_now)
        expected = Response(debug=[pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
        mock_push.assert_called_once_with(date=_now)
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'push')
    @mock.patch.object(Git, 'commit')
    @mock.patch.object(Git, 'add')
    def test_automate__with_success(self, mock_add, mock_commit, mock_push):
        adebug = Debug(msg='Call completed: \'git add .\'.')
        mock_add.return_value = Response(notify=[Notify.BASE], debug=[adebug])
        cdebug = Debug(
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(notify=[Notify.BASE], debug=[pdebug])

        plugin = self.create_plugin()
        response = plugin.automate(date=_now)
        expected = Response(
            notify=[Notify.BASE], debug=[adebug, cdebug, pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
        mock_push.assert_called_once_with(date=_now)
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Automated data push.')
        self.mock_check.assert_not_called()

    def test_commit(self):
        output = '[master 0abcd0a] Auto...\n1 files\n'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin.commit(v=True)
        msg = 'Call completed: \'git commit -m "Automated data push."\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated data push.'])
        self.mock_log.assert_not_called()

    def test_pull(self):
        output = 'remote: Counting...\nUnpacking...\n'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin.pull(v=True)
        msg = 'Call completed: \'git pull\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['git', 'pull'])
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Fetched latest changes.')

    def test_push(self):
        output = 'Counting...\nCompressing...\n'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin.push(v=True)
        msg = 'Call completed: \'git push\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_not_called()

    def test_reset(self):
        self.mock_check.return_value = {'ok': True, 'output': ''}

        plugin = self.create_plugin()
        response = plugin.reset(v=True)
        msg = 'Call completed: \'git reset --hard\'.'
        extra = {'output': ''}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        self.mock_log.assert_not_called()

    def test_status(self):
        output = 'On branch master\nYour branch...\n'
        self.mock_check.return_value = {'ok': True, 'output': output}

        plugin = self.create_plugin()
        response = plugin.status(v=True)
        msg = 'Call completed: \'git status\'.'
        extra = {'output': output}
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=extra)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['git', 'status'])
        self.mock_log.assert_not_called()


if __name__ == '__main__':
    unittest.main()
