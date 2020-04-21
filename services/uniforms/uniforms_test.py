#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for uniforms.py."""

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/uniforms', '', _path))

from common.elements.elements import ruleset  # noqa
from services.uniforms.uniforms import encoding_to_colors  # noqa
from services.uniforms.uniforms import jersey_absolute  # noqa
from services.uniforms.uniforms import jersey_colors  # noqa
from services.uniforms.uniforms import jersey_style  # noqa

BLACK = 'black'
BLUE = 'blue'
CREAM = 'cream'
GREEN = 'green'
GREY = 'grey'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
SKY = 'sky'
WHITE = 'white'
YELLOW = 'yellow'

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


def _jersey(asset, repo, tag):
    gradient = 'linear-gradient(transparent, transparent)'
    lower = asset.split('-')[0]
    return ruleset(('.' + asset), [
        ('background-image: url(\'https://brunnerj.com/fairylab/images/tea'
         'ms/{}/{}.png\')').format(lower, asset),
        ('background-image: url(\'https://gistcdn.githack.com/brunner/{}/r'
         'aw/{}/{}.svg\'), {}').format(repo, tag, asset, gradient),
    ])


def _number(font, fill, num):
    return ruleset('.number-{}-{}-{}'.format(font, fill, num), [
        ('-webkit-mask-image: url(\'https://brunnerj.com/fairylab/images/n'
         'umbers/{}/{}/{}.png\')').format(font, fill, num),
    ])


def _numbers(font):
    numbers = []
    for num in range(10):
        numbers.append(_number(font, 'solid', num))
        numbers.append(_number(font, 'border', num))
    return numbers


class UniformsTest(unittest.TestCase):
    def test_jersey_absolute__none(self):
        colors = (WHITE, '#000000', '#ffffff', 'block')
        actual = jersey_absolute('T35', colors, None, 'front', [])
        expected = ('<div class="jersey-base position-absolute whitesox-home-f'
                    'ront"></div>')
        self.assertEqual(actual, expected)

    def test_jersey_absolute__number(self):
        colors = (WHITE, '#000000', '#ffffff', 'block')
        actual = jersey_absolute('T35', colors, '1', 'back', [])
        expected = ('<div class="jersey-base position-absolute whitesox-home-b'
                    'ack"></div>\n<div class="number-base position-absolute nu'
                    'mber-block-mid number-block-solid-1 whitesox-home-solid">'
                    '</div>\n<div class="number-base position-absolute number-'
                    'block-mid number-block-border-1 whitesox-home-border"></d'
                    'iv>')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__clash_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_colors('T31', SUNDAY, 'home', BLUE)
        expected = (RED, '#000000', '#e79d94', 'diamondbacks')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__clash_true(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_colors('T31', SUNDAY, 'home', ORANGE)
        expected = (WHITE, '#cb0c29', '#000000', 'diamondbacks')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__day_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_colors('T31', SATURDAY, 'home', None)
        expected = (WHITE, '#cb0c29', '#000000', 'diamondbacks')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__day_true(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_colors('T31', SUNDAY, 'home', None)
        expected = (RED, '#000000', '#e79d94', 'diamondbacks')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__pct_false(self, mock_random):
        mock_random.return_value = 0.5

        actual = jersey_colors('T37', SUNDAY, 'home', None)
        expected = (WHITE, '#ea164c', '#000000', 'reds')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__pct_true(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_colors('T37', SUNDAY, 'home', None)
        expected = (RED, '#ffffff', '#000000', 'reds')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__team_false(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_colors('T37', SUNDAY, 'away', None)
        expected = (GREY, '#ea164c', '#000000', 'reds')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms.random.random')
    def test_jersey_colors__team_true(self, mock_random):
        mock_random.return_value = 0.3

        actual = jersey_colors('T37', SUNDAY, 'home', None)
        expected = (RED, '#ffffff', '#000000', 'reds')
        self.assertEqual(actual, expected)

    @mock.patch('services.uniforms.uniforms._encoding_to_tag')
    @mock.patch('services.uniforms.uniforms._encoding_to_repo')
    def test_jersey_style(self, mock_repo, mock_tag):
        mock_repo.return_value = 'repo'
        mock_tag.return_value = 'tag'

        colors35 = (BLUE, '#09285a', 'none', 'basic')
        colors37 = (WHITE, '#ea164c', '#000000', 'reds')
        actual = jersey_style(('T35', colors35), ('T37', colors37))
        expected = [
            _jersey('whitesox-alt-blue-back', 'repo', 'tag'),
            _jersey('whitesox-alt-blue-front', 'repo', 'tag'),
            ruleset('.whitesox-alt-blue-solid', ['background-color: #09285a']),
            _jersey('reds-home-back', 'repo', 'tag'),
            _jersey('reds-home-front', 'repo', 'tag'),
            ruleset('.reds-home-solid', ['background-color: #ea164c']),
            ruleset('.reds-home-border', ['background-color: #000000']),
        ] + _numbers('basic') + [
            ruleset('.number-basic-mid', ['left: 20px']),
            ruleset('.number-basic-l1', ['left: 16px']),
            ruleset('.number-basic-l2', ['left: 14px']),
            ruleset('.number-basic-r1', ['left: 25px']),
            ruleset('.number-basic-r2', ['left: 27px'])
        ] + _numbers('reds') + [
            ruleset('.number-reds-mid', ['left: 20px']),
            ruleset('.number-reds-l1', ['left: 16px']),
            ruleset('.number-reds-l2', ['left: 14px']),
            ruleset('.number-reds-r1', ['left: 25px']),
            ruleset('.number-reds-r2', ['left: 27px']),
            ruleset('.number-base', [
                'height: 18px',
                'width: 14px',
                '-webkit-mask-size: 14px 18px',
                'top: 18px',
            ]),
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
