#!/usr/bin/env python3
# -*- coding: utf-8 -*-

subtitle = ''

tmpl = 'recap.html'

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
    }]
}
