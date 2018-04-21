#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _team(logo, body, side):
    img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
          'reports/news/html/images/team_logos/{0}_40.png" ' + \
          'width="20" height="20" border="0" ' + \
          'class="position-absolute {1}-8p top-14p">'
    span = '<span class="d-block text-truncate align-middle p{0}-24p">{1}' + \
           '</span>'
    return img.format(logo, side) + span.format(side[0], body)


def _team_left(logo, body):
    return _team(logo, body, 'left')


def _team_right(logo, body):
    return _team(logo, body, 'right')


subtitle = ''

tmpl = 'statsplus.html'

_lal = [
    _team_left('boston_red_sox', 'Boston'), '1', '4',
    _team_right('seattle_mariners', 'Seattle', )
]
_lnl = [
    _team_left('los_angeles_dodgers', 'Los Angeles'), '4', '2',
    _team_right('san_diego_padres', 'San Diego')
]

context = {
    'title':
    'statsplus',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Statsplus'
    }],
    'live': [{
        'clazz': 'table-fixed border border-bottom-0 mt-3',
        'hcols': [' class="text-center"'],
        'bcols': [],
        'head': ['American League'],
        'body': []
    }, {
        'clazz':
        'table-fixed border',
        'hcols': [],
        'bcols': [
            ' class="position-relative w-40"', ' class="text-center w-10"',
            ' class="text-center w-10"',
            ' class="position-relative text-right w-40"'
        ],
        'head': [],
        'body': [_lal]
    }, {
        'clazz': 'table-fixed border border-bottom-0 mt-3',
        'hcols': [' class="text-center"'],
        'bcols': [],
        'head': ['National League'],
        'body': []
    }, {
        'clazz':
        'table-fixed border',
        'hcols': [],
        'bcols': [
            ' class="position-relative w-40"', ' class="text-center w-10"',
            ' class="text-center w-10"',
            ' class="position-relative text-right w-40"'
        ],
        'head': [],
        'body': [_lnl]
    }],
    'scores': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 26th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25051.html">Los Angeles Dodgers 8, San Diego Padres 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Tuesday, October 25th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25043.html">Seattle Mariners 6, Boston Red Sox 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 24th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25050.html">San Diego Padres 7, Los Angeles Dodgers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25042.html">Seattle Mariners 1, Boston Red Sox 0</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 23rd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25034.html">Boston Red Sox 3, Seattle Mariners 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25049.html">Los Angeles Dodgers 3, San Diego Padres 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 22nd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25048.html">Los Angeles Dodgers 4, San Diego Padres 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 21st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25029.html">Seattle Mariners 3, Boston Red Sox 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Thursday, October 20th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25047.html">Los Angeles Dodgers 13, San Diego Padres 7</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25024.html">Seattle Mariners 2, Boston Red Sox 0</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 19th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25046.html">San Diego Padres 2, Los Angeles Dodgers 0</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 24th, 2022'],
        'body': [[
            'C <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_48236.html">Wilson Garcia</a> was injured being hit by a pitch (San Diego Padres @ Los Angeles Dodgers)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Thursday, October 20th, 2022'],
        'body': [[
            '3B <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_22458.html">Alex Bregman</a> was injured while running the bases (Los Angeles Dodgers @ San Diego Padres)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, October 19th, 2022'],
        'body': [[
            'SP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_37102.html">Jairo Labourt</a> was injured while pitching (Seattle Mariners @ Boston Red Sox)'
        ]]
    }],
    'highlights': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_30744.html">Brad Debo</a> sets the NL playoff game record for doubles with 3 (San Diego Padres @ Los Angeles Dodgers)'
        ]]
    }],
    'forecast': []
}
