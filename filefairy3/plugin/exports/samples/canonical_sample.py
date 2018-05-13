#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _team(logo, body):
    img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
          'reports/news/html/images/team_logos/{}_40.png" ' + \
          'width="20" height="20" border="0" class="d-inline-block">'
    span = '<span class="d-inline-block align-middle px-2">{}</span>'
    body[0] = img.format(logo) + span.format(body[0])
    return body


def _secondary(t):
    return '<span class="text-secondary">' + t + '</span>'


def _success(t):
    return '<span class="text-success border px-1">' + t + '</span>'


subtitle = ''

tmpl = 'exports.html'

_t31 = _team('arizona_diamondbacks', ['Arizona', '5 - 5', 'W1'])
_t32 = _team('atlanta_braves', ['Atlanta', '10 - 0', 'W10'])
_t33 = _team('baltimore_orioles', ['Baltimore', '6 - 4', 'W1'])
_t34 = _team('boston_red_sox', ['Boston', '10 - 0', 'W10'])
_t35 = _team('chicago_white_sox', ['Chicago', '9 - 1', 'L1'])
_t36 = _team('chicago_cubs', ['Chicago', '8 - 2', 'L1'])
_t37 = _team('cincinnati_reds', ['Cincinnati', '10 - 0', 'W10'])
_t38 = _team('cleveland_indians', ['Cleveland', '8 - 2', 'W2'])
_t39 = _team('colorado_rockies', ['Colorado', '10 - 0', 'W10'])
_t40 = _team('detroit_tigers', ['Detroit', '10 - 0', 'W10'])
_t41 = _team('miami_marlins', ['Miami', '4 - 6', 'W1'])
_t42 = _team('houston_astros', ['Houston', '10 - 0', 'W10'])
_t43 = _team('kansas_city_royals', ['Kansas City', '9 - 1', 'W5'])
_t44 = _team('los_angeles_angels', ['Los Angeles', '7 - 3', 'L1'])
_t45 = _team('los_angeles_dodgers', ['Los Angeles', '5 - 5', 'W2'])
_t46 = _team('milwaukee_brewers', ['Milwaukee', '10 - 0', 'W10'])
_t47 = _team('minnesota_twins', ['Minnesota', '10 - 0', 'W10'])
_t48 = _team('new_york_yankees', ['New York', '10 - 0', 'W10'])
_t49 = _team('new_york_mets', ['New York', '8 - 2', 'L1'])
_t50 = _team('oakland_athletics', ['Oakland', '7 - 3', 'L3'])
_t51 = _team('philadelphia_phillies', ['Philadelphia', '3 - 7', 'L5'])
_t52 = _team('pittsburgh_pirates', ['Pittsburgh', '6 - 4', 'L1'])
_t53 = _team('san_diego_padres', ['San Diego', '9 - 1', 'W8'])
_t54 = _team('seattle_mariners', ['Seattle', '10 - 0', 'W10'])
_t55 = _team('san_francisco_giants', ['San Francisco', '2 - 8', 'L4'])
_t56 = _team('st_louis_cardinals', ['St. Louis', '10 - 0', 'W10'])
_t57 = _team('tampa_bay_rays', ['Tampa Bay', '10 - 0', 'W10'])
_t58 = _team('texas_rangers', ['Texas', '9 - 1', 'W9'])
_t59 = _team('toronto_blue_jays', ['Toronto', '9 - 1', 'W4'])
_t60 = _team('washington_nationals', ['Washington', '5 - 5', 'L1'])

TABLE_COLS = [''] + [' class="text-center"']*5
STANDINGS_COLS = ['class="position-relative"', ' class="text-center w-25"', ' class="text-center w-25"']

context = {
    'title':
    'exports',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Exports'
    }],
    'live': {
        'href':
        '',
        'title':
        '53%',
        'info':
        'Upcoming sim contains ' +
        ', '.join([_success('16 new'), '14 old',
                   _secondary('0 ai')]) + '.',
        'table': {
            'clazz':
            'table-sm',
            'hcols':
            TABLE_COLS,
            'bcols':
            TABLE_COLS,
            'head': [],
            'body':
            [['AL East', 'BAL', 'BOS', 'NYY', 'TB',
              'TOR'], [
                  'AL Central',
                  _success('CWS'), 'CLE',
                  _success('DET'), 'KC',
                  _success('MIN')
              ], [
                  'AL West', 'HOU',
                  _success('LAA'), 'OAK',
                  _success('SEA'),
                  _success('TEX')
              ], [
                  'NL East',
                  _success('ATL'), 'MIA',
                  _success('NYM'), 'PHI',
                  _success('WAS')
              ], [
                  'NL Central',
                  _success('CHC'),
                  _success('CIN'),
                  _success('MIL'), 'PIT',
                  _success('STL')
              ],
             ['NL West', 'ARI', 'COL',
              _success('LAD'),
              _success('SD'), 'SF']]
        },
        'ts':
        '30s ago',
        'success':
        '',
        'danger':
        ''
    },
    'standings': [{
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['AL East', 'Last 10', 'Streak'],
        'body': [_t34, _t48, _t57, _t59, _t33]
    }, {
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['AL Central', 'Last 10', 'Streak'],
        'body': [_t40, _t47, _t43, _t35, _t38]
    }, {
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['AL West', 'Last 10', 'Streak'],
        'body': [_t42, _t54, _t58, _t44, _t50]
    }, {
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['NL East', 'Last 10', 'Streak'],
        'body': [_t32, _t49, _t60, _t41, _t51]
    }, {
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['NL Central', 'Last 10', 'Streak'],
        'body': [_t37, _t46, _t56, _t36, _t52]
    }, {
        'clazz': 'border mt-3',
        'hcols': STANDINGS_COLS,
        'bcols': STANDINGS_COLS,
        'head': ['NL West', 'Last 10', 'Streak'],
        'body': [_t39, _t53, _t45, _t31, _t55]
    }]
}
