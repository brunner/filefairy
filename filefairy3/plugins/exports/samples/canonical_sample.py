#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _secondary(t):
    return '<span class="text-secondary">' + t + '</span>'


def _success(t):
    return '<span class="text-success border px-1">' + t + '</span>'


subtitle = ''

tmpl = 'exports.html'

_t33 = ['BAL', '6-4', 'W1']
_t34 = ['BOS', '10 - 0', 'W10']
_t35 = ['CWS', '9 - 1', 'L1']
_t38 = ['CLE', '8 - 2', 'W2']
_t40 = ['DET', '10 - 0', 'W10']
_t43 = ['KC', '9 - 1', 'W5']
_t47 = ['MIN', '10 - 0', 'W10']
_t48 = ['NYY', '10 - 0', 'W10']
_t57 = ['TB', '10 - 0', 'W10']
_t59 = ['TOR', '9 - 1', 'W4']
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
            'cols': [
                '', 'text-center', 'text-center', 'text-center', 'text-center',
                'text-center'
            ],
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
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL East', 'Last 10', 'Streak'],
        'body': [_t34, _t48, _t57, _t59, _t33]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL Central', 'Last 10', 'Streak'],
        'body': [_t40, _t47, _t43, _t35, _t38]
    }]
}
