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
from util.component.component import anchor  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_commit = 'https://github.com/brunner/orangeandblueleague/commit/'
_env = env()
_l = ['d-inline-block', 'w-65p']
_now = datetime.datetime(1985, 10, 27, 0, 0, 0)
_now_encoded = '1985-10-27T00:00:00'
_r = ['d-inline-block', 'text-right', 'w-65p']
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)


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

        patch_log = mock.patch('plugin.git.git.logger_.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_check = mock.patch('plugin.git.git.check_output')
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

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Git(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Git._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    @mock.patch.object(Git, 'automate')
    def test_notify__with_day(self, mock_automate):
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal(notify=Notify.FAIRYLAB_DAY)
        self.assertEqual(response, Response())

        mock_automate.assert_called_once_with(notify=Notify.FAIRYLAB_DAY)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, 'automate')
    def test_notify__with_other(self, mock_automate):
        plugin = self.create_plugin(_data())
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        mock_automate.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'pull': [], 'push': []}
        mock_home.return_value = home

        plugin = self.create_plugin(_data())
        response = plugin._render_internal(date=_now)
        index = 'html/fairylab/git/index.html'
        self.assertEqual(response, [(index, '', 'git.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    @mock.patch.object(Git, '_render')
    def test_setup(self, mock_render):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_then)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_firstlast__with_gitlog(self):
        output = 'abcdefghijklm\nnopqrstuvwxyz'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        first, last = Git._firstlast('abcdefg..nopqrst')
        self.assertEqual(first, 'abcdefghijklm')
        self.assertEqual(last, 'nopqrstuvwxyz')

        self.mock_check.assert_called_once_with(
            ['git', 'log', '-20', '--format="%H"'])
        self.mock_log.assert_not_called()

    def test_firstlast__with_match(self):
        ret = {'ok': True, 'output': '', 'stderr': ''}
        self.mock_check.return_value = ret

        first, last = Git._firstlast('abcdefg..nopqrst')
        self.assertEqual(first, 'abcdefg')
        self.assertEqual(last, 'nopqrst')

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
        output = 'ret'
        ret = {'ok': False, 'output': output}
        self.mock_check.return_value = ret

        response = Git._call(['cmd'], **{})
        msg = 'Call failed: \'cmd\'.'
        expected = Response(debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_call__with_ok_true(self):
        output = 'ret'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        response = Git._call(['cmd'], **{})
        msg = 'Call completed: \'cmd\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_check.assert_called_once_with(['cmd'])
        self.mock_log.assert_not_called()

    def test_add(self):
        output = 'ret'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.add(date=_now, v=True)
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

        plugin = self.create_plugin(_data())
        response = plugin.automate(date=_now)
        expected = Response(debug=[adebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
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
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(debug=[cdebug])

        plugin = self.create_plugin(_data())
        response = plugin.automate(date=_now)
        expected = Response(debug=[cdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
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
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(debug=[pdebug])

        plugin = self.create_plugin(_data())
        response = plugin.automate(date=_now)
        expected = Response(debug=[pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
        mock_push.assert_called_once_with(date=_now)
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
            msg='Call completed: \'git commit -m "Automated data push."\'.')
        mock_commit.return_value = Response(
            notify=[Notify.BASE], debug=[cdebug])
        pdebug = Debug(msg='Call completed: \'git push\'.')
        mock_push.return_value = Response(notify=[Notify.BASE], debug=[pdebug])

        plugin = self.create_plugin(_data())
        response = plugin.automate(date=_now)
        expected = Response(
            notify=[Notify.BASE], debug=[adebug, cdebug, pdebug])
        self.assertEqual(response, expected)

        mock_add.assert_called_once_with(date=_now)
        mock_commit.assert_called_once_with(date=_now)
        mock_push.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_check.assert_not_called()

    def test_commit__with_automated(self):
        output = '[master 0abcd0a] Auto...\n1 files\n'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.commit()
        msg = 'Call completed: \'git commit -m "Automated data push."\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Automated data push.'])
        self.mock_log.assert_not_called()

    def test_commit__with_manual(self):
        output = '[master 0abcd0a] Auto...\n1 files\n'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.commit(date=_now, v=True)
        msg = 'Call completed: \'git commit -m "Manual data push."\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(
            ['git', 'commit', '-m', 'Manual data push.'])
        self.mock_log.assert_not_called()

    @mock.patch.object(Git, '_save')
    def test_pull(self, mock_save):
        output = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.pull(date=_now, v=True)
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
    def test_push__with_automated(self, mock_save):
        output = 'To github.com...\n'
        ret = {'ok': True, 'output': '', 'stderr': output}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.push(date=_now)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_called_once_with(
            response, 'push', Git._stderr, date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Automated data push.')

    @mock.patch.object(Git, '_save')
    def test_push__with_manual(self, mock_save):
        output = 'To github.com...\n'
        ret = {'ok': True, 'output': '', 'stderr': output}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.push(date=_now, v=True)
        msg = 'Call completed: \'git push\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        mock_save.assert_called_once_with(
            response, 'push', Git._stderr, date=_now, v=True)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'push'])
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Manual data push.')

    def test_reset(self):
        ret = {'ok': True, 'output': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.reset(date=_now, v=True)
        msg = 'Call completed: \'git reset --hard\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'reset', '--hard'])
        self.mock_log.assert_not_called()

    def test_status(self):
        output = 'On branch master\nYour branch...\n'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        self.mock_check.return_value = ret

        plugin = self.create_plugin(_data())
        response = plugin.status(date=_now, v=True)
        msg = 'Call completed: \'git status\'.'
        expected = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])
        self.assertEqual(response, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_check.assert_called_once_with(['git', 'status'])
        self.mock_log.assert_not_called()

    def test_home__with_empty(self):
        plugin = self.create_plugin(_data())
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Git'
        }]
        expected = {'breadcrumbs': breadcrumbs}
        self.assertEqual(actual, expected)

    def test_home__with_pull(self):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        plugin = self.create_plugin(
            _data(pull=[{
                'date': _now_encoded,
                'first': first,
                'last': last
            }]))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Git'
        }]
        ffirst = span(_l, anchor(_commit + 'abcdefghijklm', 'abcdefg'))
        flast = span(_r, anchor(_commit + 'nopqrstuvwxyz', 'nopqrst'))
        pull = table(
            clazz='border mt-3',
            head=['Range', 'Date', 'Time'],
            body=[[ffirst + ' ... ' + flast, 'Oct 27', '00:00']])
        expected = {'breadcrumbs': breadcrumbs, 'pull': pull}
        self.assertEqual(actual, expected)

    def test_home__with_push(self):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        plugin = self.create_plugin(
            _data(push=[{
                'date': _now_encoded,
                'first': first,
                'last': last
            }]))
        actual = plugin._home(date=_now)
        breadcrumbs = [{
            'href': '/fairylab/',
            'name': 'Home'
        }, {
            'href': '',
            'name': 'Git'
        }]
        ffirst = span(_l, anchor(_commit + 'abcdefghijklm', 'abcdefg'))
        flast = span(_r, anchor(_commit + 'nopqrstuvwxyz', 'nopqrst'))
        push = table(
            clazz='border mt-3',
            head=['Range', 'Date', 'Time'],
            body=[[ffirst + ' ... ' + flast, 'Oct 27', '00:00']])
        expected = {'breadcrumbs': breadcrumbs, 'push': push}
        self.assertEqual(actual, expected)

    @mock.patch.object(Git, '_render')
    @mock.patch.object(Git, '_firstlast')
    def test_save__with_pull(self, mock_firstlast, mock_render):
        first, last = 'abcdefghijklm', 'nopqrstuvwxyz'
        mock_firstlast.return_value = (first, last)

        output = 'remote: Counting...\nUnpacking...\n'
        ret = {'ok': True, 'output': output, 'stderr': ''}
        msg = 'Call completed: \'git pull\'.'
        response = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])

        plugin = self.create_plugin(_data())
        plugin._save(response, 'pull', Git._stdout, date=_now, v=True)

        write = _data(pull=[{
            'date': _now_encoded,
            'first': first,
            'last': last
        }])
        mock_firstlast.assert_called_once_with(output)
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

        output = 'To github.com...\n'
        ret = {'ok': True, 'output': '', 'stderr': output}
        msg = 'Call completed: \'git pull\'.'
        response = Response(
            notify=[Notify.BASE], debug=[Debug(msg=msg, extra=ret)])

        plugin = self.create_plugin(_data())
        plugin._save(response, 'push', Git._stderr, date=_now, v=True)

        write = _data(push=[{
            'date': _now_encoded,
            'first': first,
            'last': last
        }])
        mock_firstlast.assert_called_once_with(output)
        mock_render.assert_called_once_with(date=_now, v=True)
        self.mock_open.assert_called_once_with(Git._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_check.assert_not_called()
        self.mock_log.assert_not_called()


if __name__ in ['__main__', 'plugin.git.git_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.git'
    _pth = 'plugin/git'
    main(GitTest, Git, _pkg, _pth, {}, _main, date=_now, e=_env)
