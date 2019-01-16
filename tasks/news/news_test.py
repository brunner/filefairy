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
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.news.news import News  # noqa

ENV = env()

DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

EXTRACT_DIR = re.sub(r'/tasks/news', '/resource/extract', _path)
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')

TESTDATA = get_testdata()


class NewsTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, read):
        mo = mock.mock_open(read_data=dumps(read))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_news(self):
        self.init_mocks({})
        news = News(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(News._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.assertEqual(news.data, {})

        self.reset_mocks()
        self.init_mocks({})

        return news

    @mock.patch.object(News, '_index_html')
    def test_render_data(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        news = self.create_news()
        actual = news._render_data(date=DATE_10260602)
        expected = [('news/index.html', '', 'news.html', index_html)]
        self.assertEqual(actual, expected)

        mock_index.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(News, '_render')
    def test_notify__statsplus_finish(self, mock_render):
        news = self.create_news()
        response = news._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(News, '_render')
    def test_notify__other(self, mock_render):
        news = self.create_news()
        response = news._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_render, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(News, '_tables')
    def test_index_html(self, mock_tables):
        table_ = table(head=[[cell(content='Wednesday')]])
        mock_tables.return_value = table_

        news = self.create_news()
        actual = news._index_html(date=DATE_10260602)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'News'
        }]
        expected = {
            'breadcrumbs': breadcrumbs,
            'injuries': table_,
            'news': table_,
            'transactions': table_,
        }
        self.assertEqual(actual, expected)

        mock_tables.assert_has_calls([
            mock.call('injuries'),
            mock.call('news'),
            mock.call('transactions')
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch('tasks.news.news.loads')
    def test_tables(self, mock_loads):
        mock_loads.side_effect = [
            json.loads(TESTDATA['injuries.json']),
            json.loads(TESTDATA['news.json']),
            json.loads(TESTDATA['transactions.json']),
        ]

        news = self.create_news()
        for name in ['injuries', 'news', 'transactions']:
            actual = news._tables(name)
            expected = json.loads(TESTDATA[name + '_tables.json'])
            self.assertEqual(actual, expected)

        mock_loads.assert_has_calls([
            mock.call(os.path.join(EXTRACT_LEAGUES, 'injuries.json')),
            mock.call(os.path.join(EXTRACT_LEAGUES, 'news.json')),
            mock.call(os.path.join(EXTRACT_LEAGUES, 'transactions.json')),
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)


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
