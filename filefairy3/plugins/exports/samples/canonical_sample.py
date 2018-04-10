#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _secondary(t):
    return '<span class="text-secondary">' + t + '</span>'


def _success(t):
    return '<span class="text-success border px-1">' + t + '</span>'


subtitle = ''

tmpl = 'exports.html'

_t31 = ['ARI', '5 - 5', 'W1']
_t32 = ['ATL', '10 - 0', 'W10']
_t33 = ['BAL', '6 - 4', 'W1']
_t34 = ['BOS', '10 - 0', 'W10']
_t35 = ['CWS', '9 - 1', 'L1']
_t36 = ['CHC', '8 - 2', 'L1']
_t37 = ['CIN', '10 - 0', 'W10']
_t38 = ['CLE', '8 - 2', 'W2']
_t39 = ['COL', '10 - 0', 'W10']
_t40 = ['DET', '10 - 0', 'W10']
_t41 = ['MIA', '4 - 6', 'W1']
_t42 = ['HOU', '10 - 0', 'W10']
_t43 = ['KC', '9 - 1', 'W5']
_t44 = ['LAA', '7 - 3', 'L1']
_t45 = ['LAD', '5 - 5', 'W2']
_t46 = ['MIL', '10 - 0', 'W10']
_t47 = ['MIN', '10 - 0', 'W10']
_t48 = ['NYY', '10 - 0', 'W10']
_t49 = ['NYM', '8 - 2', 'L1']
_t50 = ['OAK', '7 - 3', 'L3']
_t51 = ['PHI', '3 - 7', 'L5']
_t52 = ['PIT', '6 - 4', 'L1']
_t53 = ['SD', '9 - 1', 'W8']
_t54 = ['SEA', '10 - 0', 'W10']
_t55 = ['SF', '2 - 8', 'L4']
_t56 = ['STL', '10 - 0', 'W10']
_t57 = ['TB', '10 - 0', 'W10']
_t58 = ['TEX', '9 - 1', 'W9']
_t59 = ['TOR', '9 - 1', 'W4']
_t60 = ['WAS', '5 - 5', 'L1']

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
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL West', 'Last 10', 'Streak'],
        'body': [_t42, _t54, _t58, _t44, _t50]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL East', 'Last 10', 'Streak'],
        'body': [_t32, _t49, _t60, _t41, _t51]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL Central', 'Last 10', 'Streak'],
        'body': [_t37, _t46, _t56, _t36, _t52]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL West', 'Last 10', 'Streak'],
        'body': [_t39, _t53, _t45, _t31, _t55]
    }]
}
