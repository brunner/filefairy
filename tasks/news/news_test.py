#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/news', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa
from tasks.news.news import News  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

EXTRACT_DIR = re.sub(r'/tasks/news', '/resources/extract', _path)
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')

TESTDATA = get_testdata()


class NewsTest(Test):
    def setUp(self):
        open_patch = mock.patch('common.io_.io_.open', create=True)
        self.addCleanup(open_patch.stop)
        self.open_ = open_patch.start()

    def init_mocks(self, read):
        mo = mock.mock_open(read_data=dumps(read))
        self.open_handle_ = mo()
        self.open_.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.open_handle_.write.reset_mock()

    def create_news(self):
        self.init_mocks({})
        news = News(date=DATE_10260602, e=ENV)

        self.open_handle_.write.assert_not_called()
        self.assertEqual(news.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return news

    @mock.patch.object(News, 'get_news_html')
    def test_render_data(self, get_news_html_):
        news_html = {'injuries': []}
        get_news_html_.return_value = news_html

        news = self.create_news()
        actual = news._render_data(date=DATE_10260602)
        expected = [('news/index.html', '', 'news.html', news_html)]
        self.assertEqual(actual, expected)

        get_news_html_.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(News, '_render')
    def test_notify__statsplus_finish(self, _render_):
        news = self.create_news()
        response = news._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        _render_.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(News, '_render')
    def test_notify__other(self, _render_):
        news = self.create_news()
        response = news._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(_render_, self.open_handle_.write)

    @mock.patch('tasks.news.news.loads')
    def test_tables(self, loads_):
        loads_.side_effect = [
            json.loads(TESTDATA['injuries.json']),
            json.loads(TESTDATA['news.json']),
            json.loads(TESTDATA['transactions.json']),
        ]

        news = self.create_news()
        for name in ['injuries', 'news', 'transactions']:
            actual = news.create_tables(name)
            expected = json.loads(TESTDATA[name + '_tables.json'])
            self.assertEqual(actual, expected)

        loads_.assert_has_calls([
            mock.call(os.path.join(EXTRACT_LEAGUES, 'injuries.json')),
            mock.call(os.path.join(EXTRACT_LEAGUES, 'news.json')),
            mock.call(os.path.join(EXTRACT_LEAGUES, 'transactions.json')),
        ])
        self.assertNotCalled(self.open_handle_.write)

    @mock.patch.object(News, 'create_tables')
    def test_get_news_html(self, create_tables_):
        table_ = table(head=[row(cells=[cell(content='Wednesday')])])
        create_tables_.return_value = table_

        news = self.create_news()
        actual = news.get_news_html(date=DATE_10260602)
        expected = {
            'injuries': table_,
            'news': table_,
            'transactions': table_,
        }
        self.assertEqual(actual, expected)

        create_tables_.assert_has_calls([
            mock.call('injuries'),
            mock.call('news'),
            mock.call('transactions')
        ])
        self.assertNotCalled(self.open_handle_.write)


if __name__ in ['__main__', 'tasks.news.news_test']:
    main(
        NewsTest,
        News,
        'tasks.news',
        'tasks/news',
        {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV,
    )
