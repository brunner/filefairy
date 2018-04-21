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

_lws = [
    _team_left('los_angeles_dodgers', 'Los Angeles'), '2', '4',
    _team_right('seattle_mariners', 'Seattle')
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
        'head': ['World Series'],
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
        'body': [_lws]
    }],
    'scores': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, November 4th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25072.html">Seattle Mariners 13, Los Angeles Dodgers 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Wednesday, November 2nd, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25071.html">Seattle Mariners 5, Los Angeles Dodgers 3</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Tuesday, November 1st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25052.html">Seattle Mariners 3, Los Angeles Dodgers 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 31st, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25045.html">Los Angeles Dodgers 5, Seattle Mariners 4</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 29th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25044.html">Seattle Mariners 5, Los Angeles Dodgers 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 28th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_25041.html">Los Angeles Dodgers 5, Seattle Mariners 3</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, October 31st, 2022'],
        'body': [[
            'RP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_19570.html">Josh Outman</a> was injured while pitching (Los Angeles Dodgers @ Seattle Mariners)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Friday, October 28th, 2022'],
        'body': [[
            'SP <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_33236.html">Mario Ram?rez</a> was injured while pitching (Seattle Mariners @ Los Angeles Dodgers)'
        ]]
    }],
    'highlights': [],
    'forecast': []
}
