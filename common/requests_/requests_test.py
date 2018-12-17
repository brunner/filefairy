#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/requests_', '', _path))
from common.requests_.requests_ import get  # noqa


class RequestsTest(unittest.TestCase):
    @mock.patch('common.requests_.requests_._logger.log')
    @mock.patch('common.requests_.requests_.requests.get')
    def test_get__error(self, mock_get, mock_log):
        mock_get.return_value.status_code = 403

        actual = get('http://url')
        self.assertEqual(actual, '')

        mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)
        mock_get.assert_called_once_with('http://url', timeout=10)

    @mock.patch('common.requests_.requests_._logger.log')
    @mock.patch('common.requests_.requests_.requests.get')
    def test_get__exception(self, mock_get, mock_log):
        mock_get.side_effect = Exception()

        actual = get('http://url')
        self.assertEqual(actual, '')

        mock_log.assert_called_once_with(
            logging.WARNING, 'Handled warning.', exc_info=True)
        mock_get.assert_called_once_with('http://url', timeout=10)

    @mock.patch('common.requests_.requests_._logger.log')
    @mock.patch('common.requests_.requests_.requests.get')
    def test_get__ok(self, mock_get, mock_log):
        expected = 'response'
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = expected

        actual = get('http://url')
        self.assertEqual(actual, expected)

        mock_log.assert_not_called()
        mock_get.assert_called_once_with('http://url', timeout=10)


if __name__ == '__main__':
    unittest.main()
