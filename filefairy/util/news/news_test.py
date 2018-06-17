#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/news', '', _path)
sys.path.append(_root)
from util.news.news import box_scores  # noqa

_now = datetime.datetime(2022, 10, 16)
_then = datetime.datetime(2022, 10, 9)

_box_sub = '<html> <title>MLB Box Scores, Arizona Diamondbacks at Lo' + \
           's Angeles Dodgers, {}</title> </html>'
_box_here = os.path.join(_root, 'resource/download/news/html/box_scores')
_box_there = os.path.join(_root, 'resource/extract/box_scores')
_game = '[%T]\tTop of the 1st -  Arizona Diamondbacks batting'
_game_here = os.path.join(_root, 'resource/download/news/txt/leagues')
_game_there = os.path.join(_root, 'resource/extract/game_logs')


class NewsTest(unittest.TestCase):
    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.listdir')
    @mock.patch('util.news.news.os.path.isfile')
    def test_box_scores__with_now_date(self, mock_isfile, mock_listdir,
                                       mock_open, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html']
        box = _box_sub.format('10/15/2022')
        mo_box_here = mock.mock_open(read_data=box)
        mo_box_there = mock.mock_open(read_data='')
        mock_handle_box_there = mo_box_there()
        mo_game_here = mock.mock_open(read_data=_game)
        mo_game_there = mock.mock_open(read_data='')
        mock_handle_game_there = mo_game_there()
        mock_open.side_effect = [
            mo_box_here.return_value, mo_game_here.return_value,
            mo_box_there.return_value, mo_game_there.return_value
        ]

        actual = box_scores(_then)
        self.assertEqual(actual, _now)

        box_here_123 = os.path.join(_box_here, 'game_box_123.html')
        box_there_123 = os.path.join(_box_there, 'game_box_123.html')
        game_here_123 = os.path.join(_game_here, 'log_123.txt')
        game_there_123 = os.path.join(_game_there, 'log_123.txt')
        isfile_calls = [
            mock.call(box_here_123),
            mock.call(game_here_123),
        ]
        mock_isfile.assert_has_calls(isfile_calls)
        mock_listdir.assert_called_once_with(_box_here)
        open_calls = [
            mock.call(box_here_123, 'r', encoding='iso-8859-1'),
            mock.call(game_here_123, 'r', encoding='iso-8859-1'),
            mock.call(box_there_123, 'w'),
            mock.call(game_there_123, 'w')
        ]
        mock_open.assert_has_calls(open_calls)
        mock_handle_box_there.write.assert_called_once_with(box)
        mock_handle_game_there.write.assert_called_once_with(_game)
        calls = [mock.call(_box_there), mock.call(_game_there)]
        mock_recreate.assert_has_calls(calls)

    @mock.patch('util.news.news.recreate')
    @mock.patch('util.news.news.open', create=True)
    @mock.patch('util.news.news.os.listdir')
    @mock.patch('util.news.news.os.path.isfile')
    def test_box_scores__with_then_date(self, mock_isfile, mock_listdir,
                                        mock_open, mock_recreate):
        mock_isfile.return_value = True
        mock_listdir.return_value = ['game_box_123.html']
        box = _box_sub.format('10/01/2022')
        mo_box_here = mock.mock_open(read_data=box)
        mo_game_here = mock.mock_open(read_data=_game)
        mock_open.side_effect = [
            mo_box_here.return_value, mo_game_here.return_value
        ]

        actual = box_scores(_then)
        self.assertEqual(actual, _then)

        box_here_123 = os.path.join(_box_here, 'game_box_123.html')
        game_here_123 = os.path.join(_game_here, 'log_123.txt')
        isfile_calls = [
            mock.call(box_here_123),
            mock.call(game_here_123),
        ]
        mock_isfile.assert_has_calls(isfile_calls)
        mock_listdir.assert_called_once_with(_box_here)
        open_calls = [
            mock.call(box_here_123, 'r', encoding='iso-8859-1'),
            mock.call(game_here_123, 'r', encoding='iso-8859-1')
        ]
        mock_open.assert_has_calls(open_calls)
        calls = [mock.call(_box_there), mock.call(_game_there)]
        mock_recreate.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
