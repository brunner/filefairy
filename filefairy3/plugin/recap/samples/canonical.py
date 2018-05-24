#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/statsplus/samples', '', _path)
sys.path.append(_root)
from util.component.component import table  # noqa
from util.team.team import logo_absolute  # noqa

subtitle = ''

tmpl = 'recap.html'

_cols = [
    'class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
]

context = {
    'title':
    'recap',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Recap'
    }],
    'injuries': [{
        'clazz': 'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, July 4th, 2022'],
        'body': [[
            'Pittsburgh Pirates: <a href="../players/player_35155.html">John Barbato</a> diagnosed with a sore forearm, is day-to-day for 5 days.'
        ]]
    }, {
        'clazz': 'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, July 3th, 2022'],
        'body': [[
            'Los Angeles Angels: SP <a href="../players/player_37318.html">Ty Blach</a> was injured while pitching.  The Diagnosis: back stiffness. This is a day-to-day injury expected to last 5 days.'
        ], [
            'Washington Nationals: RP <a href="../players/player_32624.html">Hunter Strickland</a> was injured while pitching.  The Diagnosis: back spasms. This is a day-to-day injury expected to last 5 days.'
        ], [
            'Tampa Bay Rays: RP <a href="../players/player_1958.html">Javier Medina</a> was injured while pitching.  The diagnosis is not yet known.'
        ], [
            'Pittsburgh Pirates: SP <a href="../players/player_35155.html">John Barbato</a> was injured while pitching.  The diagnosis is not yet known.'
        ], [
            'Pittsburgh Pirates: CF <a href="../players/player_1604.html">Carl Chester</a> was injured on a defensive play.  The diagnosis is not yet known.'
        ], [
            'Detroit Tigers: RP <a href="../players/player_22457.html">Walker Buehler</a> was injured while pitching.  The diagnosis is not yet known.'
        ]]
    }],
    'news': [{
        'clazz': 'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, July 4th, 2022'],
        'body': [[
            '1B <a href="../players/player_33892.html">Viosergy Rosa</a> of the Chicago White Sox honored: Wins the MLB AL Player of the Week Award.'
        ], [
            '1B <a href="../players/player_27194.html">Freddie Freeman</a> of the Atlanta Braves honored: Wins the MLB NL Player of the Week Award.'
        ]]
    }],
    'transactions': [{
        'clazz': 'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Monday, July 4th, 2022'],
        'body': [[
            'San Diego Padres: Signed <a href="../players/player_56862.html">Antonio Marquis</a> to a minor league contract with a signing bonus of $180,000.'
        ], [
            'The Detroit Tigers traded 25-year-old minor league left fielder <a href="../players/player_28672.html">Nick Plummer</a> to the Milwaukee Brewers, getting 33-year-old closer <a href="../players/player_36352.html">Phil Klein</a> in return.'
        ], [
            'The Detroit Tigers traded 25-year-old minor league left fielder <a href="../players/player_25202.html">Wesley Rodriguez</a> and 31-year-old left fielder <a href="../players/player_33588.html">Michael A. Taylor</a> to the Chicago Cubs, getting 30-year-old right fielder <a href="../players/player_35161.html">Drew Vettleson</a> in return.'
        ], [
            'The Detroit Tigers traded 21-year-old minor league shortstop <a href="../players/player_32327.html">Jesus Martinez</a> to the Philadelphia Phillies, getting 28-year-old left fielder <a href="../players/player_37237.html">Mitch Nay</a> in return.'
        ], [
            'The Minnesota Twins traded 25-year-old first baseman <a href="../players/player_39581.html">Lewin Diaz</a> to the Chicago Cubs, getting 30-year-old starting pitcher <a href="../players/player_37975.html">Matt Anderson</a>, 19-year-old minor league starting pitcher <a href="../players/player_22921.html">Juan Monreal</a> and 21-year-old minor league catcher <a href="../players/player_55093.html">Jonathan Salazar</a> in return.'
        ]]
    }],
    'standings': [
            table(
                hcols=_cols,
                bcols=_cols,
                head=['AL East', 'W', 'L'],
                body=[[logo_absolute('34', 'Boston', 'left'), '99', '63'], [
                    logo_absolute('48', 'New York', 'left'), '88', '74'
                ], [logo_absolute('59', 'Toronto', 'left'), '73', '89'],
                      [logo_absolute('33', 'Baltimore', 'left'), '70', '92'],
                      [logo_absolute('57', 'Tampa Bay', 'left'), '65', '97']]),
            table(
                hcols=_cols,
                bcols=_cols,
                head=['AL Central', 'W', 'L'],
                body=[[logo_absolute('47', 'Minnesota', 'left'), '88', '74'], [
                    logo_absolute('40', 'Detroit', 'left'), '86', '76'
                ], [logo_absolute('35', 'Chicago', 'left'), '82', '80'], [
                    logo_absolute('38', 'Cleveland', 'left'), '76', '86'
                ], [logo_absolute('43', 'Kansas City', 'left'), '76', '86']]),
            table(
                hcols=_cols,
                bcols=_cols,
                head=['AL West', 'W', 'L'],
                body=[[logo_absolute('54', 'Seattle', 'left'), '98', '64'], [
                    logo_absolute('42', 'Houston', 'left'), '85', '77'
                ], [logo_absolute('50', 'Oakland', 'left'), '75', '87'],
                      [logo_absolute('44', 'Los Angeles', 'left'), '70', '92'],
                      [logo_absolute('58', 'Texas', 'left'), '67', '95']]),
            table(
                hcols=_cols,
                bcols=_cols,
                head=['NL East', 'W', 'L'],
                body=[[logo_absolute('49', 'New York', 'left'), '95', '67'], [
                    logo_absolute('41', 'Miami', 'left'), '84', '78'
                ], [logo_absolute('32', 'Atlanta', 'left'), '77', '85'], [
                    logo_absolute('51', 'Philadelphia', 'left'), '75', '87'
                ], [logo_absolute('60', 'Washington', 'left'), '73', '89']]),
            table(
                hcols=_cols,
                bcols=_cols,
                head=['NL Central', 'W', 'L'],
                body=[[logo_absolute('37', 'Cincinnati', 'left'), '111', '51'],
                      [logo_absolute('56', 'St. Louis', 'left'), '89', '73'], [
                          logo_absolute('46', 'Milwaukee', 'left'), '77', '85'
                      ], [logo_absolute('36', 'Chicago', 'left'), '71', '91'],
                      [logo_absolute('52', 'Pittsburgh', 'left'), '53',
                       '109']]),
            table(
                hcols=_cols,
                bcols=_cols,
                head=['NL West', 'W', 'L'],
                body=[[logo_absolute('53', 'San Diego', 'left'), '104', '58'],
                      [logo_absolute('45', 'Los Angeles', 'left'), '97', '65'],
                      [logo_absolute('39', 'Colorado', 'left'), '88', '74'],
                      [logo_absolute('31', 'Arizona', 'left'), '76', '86'], [
                          logo_absolute('55', 'San Francisco', 'left'), '62',
                          '100'
                      ]])
        ]
}
