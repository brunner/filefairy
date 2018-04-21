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


subtitle = ''

tmpl = 'statsplus.html'

_l31 = _team_left('arizona_diamondbacks', '4-3')
_l32 = _team_left('atlanta_braves', '5-1')
_l33 = _team_left('baltimore_orioles', '0-6')
_l34 = _team_left('boston_red_sox', '4-3')
_l35 = _team_left('chicago_white_sox', '3-3')
_l36 = _team_left('chicago_cubs', '3-4')
_l37 = _team_left('cincinnati_reds', '3-3')
_l38 = _team_left('cleveland_indians', '1-4')
_l39 = _team_left('colorado_rockies', '2-3')
_l40 = _team_left('detroit_tigers', '4-3')
_l41 = _team_left('miami_marlins', '2-5')
_l42 = _team_left('houston_astros', '5-2')
_l43 = _team_left('kansas_city_royals', '4-3')
_l44 = _team_left('los_angeles_angels', '3-3')
_l45 = _team_left('los_angeles_dodgers', '4-2')
_l46 = _team_left('milwaukee_brewers', '2-4')
_l47 = _team_left('minnesota_twins', '4-3')
_l48 = _team_left('new_york_yankees', '4-2')
_l49 = _team_left('new_york_mets', '5-1')
_l50 = _team_left('oakland_athletics', '4-3')
_l51 = _team_left('philadelphia_phillies', '5-2')
_l52 = _team_left('pittsburgh_pirates', '1-5')
_l53 = _team_left('san_diego_padres', '4-2')
_l54 = _team_left('seattle_mariners', '2-5')
_l55 = _team_left('san_francisco_giants', '2-5')
_l56 = _team_left('st_louis_cardinals', '6-0')
_l57 = _team_left('tampa_bay_rays', '4-3')
_l58 = _team_left('texas_rangers', '3-3')
_l59 = _team_left('toronto_blue_jays', '2-4')
_l60 = _team_left('washington_nationals', '1-6')

_s31 = [_team_left('arizona_diamondbacks', 'Arizona'), '76', '86', '28', '']
_s32 = [_team_left('atlanta_braves', 'Atlanta'), '77', '85', '18', '']
_s33 = [_team_left('baltimore_orioles', 'Baltimore'), '70', '92', '29', '']
_s34 = [_team_left('boston_red_sox', 'Boston'), '99', '63', '-', 'X']
_s35 = [_team_left('chicago_white_sox', 'Chicago'), '82', '80', '6', '']
_s36 = [_team_left('chicago_cubs', 'Chicago'), '71', '91', '40', '']
_s37 = [_team_left('cincinnati_reds', 'Cincinnati'), '111', '51', '-', 'X']
_s38 = [_team_left('cleveland_indians', 'Cleveland'), '76', '86', '12', '']
_s39 = [_team_left('colorado_rockies', 'Colorado'), '88', '74', '16', '']
_s40 = [_team_left('detroit_tigers', 'Detroit'), '86', '76', '2', '']
_s41 = [_team_left('miami_marlins', 'Miami'), '84', '78', '11', '']
_s42 = [_team_left('houston_astros', 'Houston'), '85', '77', '13', '']
_s43 = [_team_left('kansas_city_royals', 'Kansas City'), '76', '86', '12', '']
_s44 = [_team_left('los_angeles_angels', 'Los Angeles'), '70', '92', '28', '']
_s45 = [_team_left('los_angeles_dodgers', 'Los Angeles'), '97', '65', '7', '']
_s46 = [_team_left('milwaukee_brewers', 'Milwaukee'), '77', '85', '34', '']
_s47 = [_team_left('minnesota_twins', 'Minnesota'), '88', '74', '-', 'X']
_s48 = [_team_left('new_york_yankees', 'New York'), '88', '74', '11', '']
_s49 = [_team_left('new_york_mets', 'New York'), '95', '67', '-', 'X']
_s50 = [_team_left('oakland_athletics', 'Oakland'), '75', '87', '23', '']
_s51 = [
    _team_left('philadelphia_phillies', 'Philadelphia'), '75', '87', '20', ''
]
_s52 = [_team_left('pittsburgh_pirates', 'Pittsburgh'), '53', '109', '58', '']
_s53 = [_team_left('san_diego_padres', 'San Diego'), '104', '58', '-', 'X']
_s54 = [_team_left('seattle_mariners', 'Seattle'), '98', '64', '-', 'X']
_s55 = [
    _team_left('san_francisco_giants', 'San Francisco'), '62', '100', '42', ''
]
_s56 = [_team_left('st_louis_cardinals', 'St. Louis'), '89', '73', '22', '']
_s57 = [_team_left('tampa_bay_rays', 'Tampa Bay'), '65', '97', '34', '']
_s58 = [_team_left('texas_rangers', 'Texas'), '67', '95', '31', '']
_s59 = [_team_left('toronto_blue_jays', 'Toronto'), '73', '89', '26', '']
_s60 = [_team_left('washington_nationals', 'Washington'), '73', '89', '22', '']

_w35 = [_team_left('chicago_white_sox', 'Chicago'), '82', '80', '4', '']
_w39 = [_team_left('colorado_rockies', 'Colorado'), '88', '74', '1', '']
_w40 = [_team_left('detroit_tigers', 'Detroit'), '86', '76', '-', 'X']
_w41 = [_team_left('miami_marlins', 'Miami'), '84', '78', '5', '']
_w42 = [_team_left('houston_astros', 'Houston'), '85', '77', '1', '']
_w45 = [_team_left('los_angeles_dodgers', 'Los Angeles'), '97', '65', '-', 'X']
_w48 = [_team_left('new_york_yankees', 'New York'), '88', '74', '+2', 'X']
_w56 = [_team_left('st_louis_cardinals', 'St. Louis'), '89', '73', '-', 'X']

LIVE_BCOL = ' class="td-sm position-relative text-center w-20"'
FORE_COLS = [
    ' class="position-relative text-truncate"', ' class="text-right w-55p"',
    ' class="text-right w-55p"', ' class="text-right w-55p"',
    ' class="text-right w-55p"'
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
        'bcols': [LIVE_BCOL] * 5,
        'head': [],
        'body': [[_l48, _l34, _l57, _l59,
                  _l33], [_l40, _l43, _l47, _l35, _l38],
                 [_l42, _l50, _l44, _l58, _l54]]
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
        'bcols': [LIVE_BCOL] * 5,
        'head': [],
        'body': [[_l32, _l49, _l51, _l41,
                  _l60], [_l56, _l37, _l36, _l46, _l52],
                 [_l45, _l53, _l31, _l39, _l55]]
    }],
    'scores': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 9th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2998.html">Arizona Diamondbacks 4, Los Angeles Dodgers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3003.html">Atlanta Braves 2, Los Angeles Angels 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2996.html">Cincinnati Reds 7, Milwaukee Brewers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3002.html">Detroit Tigers 11, Chicago White Sox 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2993.html">Houston Astros 7, Seattle Mariners 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2991.html">Kansas City Royals 8, Cleveland Indians 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_14721.html">Miami Marlins 6, Chicago Cubs 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3001.html">New York Mets 1, San Francisco Giants 0</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_3000.html">New York Yankees 5, Baltimore Orioles 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2992.html">Philadelphia Phillies 3, Washington Nationals 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2999.html">San Diego Padres 8, Colorado Rockies 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2990.html">St. Louis Cardinals 5, Pittsburgh Pirates 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2997.html">Tampa Bay Rays 12, Boston Red Sox 9</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2994.html">Texas Rangers 5, Oakland Athletics 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2995.html">Toronto Blue Jays 8, Minnesota Twins 2</a>'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2979.html">Atlanta Braves 10, Los Angeles Angels 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2984.html">Boston Red Sox 10, Tampa Bay Rays 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2975.html">Chicago Cubs 10, Miami Marlins 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2977.html">Chicago White Sox 5, Detroit Tigers 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2983.html">Cincinnati Reds 8, Milwaukee Brewers 0</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2989.html">Cleveland Indians 3, Kansas City Royals 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2976.html">Houston Astors 6, Seattle Mariners 3</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2978.html">Los Angeles Dodgers 5, Arizona Diamondbacks 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2981.html">Minnesota Twins 10, Toronto Blue Jays 7</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2987.html">New York Yankees 5, Baltimore Orioles 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2982.html">Philadelphia Phillies 3, Washington Nationals 2</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2986.html">San Diego Padres 6, Colorado Rockies 5</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2985.html">San Francisco Giants 5, New York Mets 4</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2988.html">St. Louis Cardinals 4, Pittsburgh Pirates 1</a>'
        ], [
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/box_scores/game_box_2980.html">Texas Rangers 9, Oakland Athletics 1</a>'
        ]]
    }],
    'injuries': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Sunday, October 9th, 2022'],
        'body': [[
            'RF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_36649.html">Elier Hernandez</a> was injured while running the bases (Cleveland Indians @ Kansas City Royals)'
        ], [
            'RF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_34118.html">Gregory Polanco</a> was injured on a defensive play (Milwaukee Brewers @ Cincinnati Reds)'
        ], [
            'SS <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_30016.html">Austin Bodrato</a> was injured while running the bases (Milwaukee Brewers @ Cincinnati Reds)'
        ]]
    }, {
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '3B <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_33777.html">Kaleb Cowart</a> was injured in a collision at a base (Cleveland Indians @ Kansas City Royals)'
        ], [
            'LF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_29996.html">Keon Broxton</a> was injured while throwing the ball (Houston Astros @ Seattle Mariners)'
        ], [
            'LF <a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_26747.html">Desmond Lindsay</a> was injured on a defensive play (New York Yankees @ Baltimore Orioles)'
        ]]
    }],
    'highlights': [{
        'clazz':
        'border mt-3',
        'hcols': [''],
        'bcols': [''],
        'head': ['Saturday, October 8th, 2022'],
        'body': [[
            '<a href="https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/players/player_38868.html">Connor Harrell</a> ties the BOS regular season game record for runs with 4 (Boston Red Sox @ Tampa Bay Rays)'
        ]]
    }],
    'forecast': [{
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL East', 'W', 'L', 'GB', 'M#'],
        'body': [_s34, _s48, _s59, _s33, _s57]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL Central', 'W', 'L', 'GB', 'M#'],
        'body': [_s47, _s40, _s35, _s38, _s43]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL West', 'W', 'L', 'GB', 'M#'],
        'body': [_s54, _s42, _s50, _s44, _s58]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['AL Wild Card', 'W', 'L', 'GB', 'M#'],
        'body': [_w48, _w40, _w42, _w35]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL East', 'W', 'L', 'GB', 'M#'],
        'body': [_s49, _s41, _s32, _s51, _s60]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL Central', 'W', 'L', 'GB', 'M#'],
        'body': [_s37, _s56, _s46, _s36, _s52]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL West', 'W', 'L', 'GB', 'M#'],
        'body': [_s53, _s45, _s39, _s31, _s55]
    }, {
        'clazz': 'table-fixed border mt-3',
        'hcols': FORE_COLS,
        'bcols': FORE_COLS,
        'head': ['NL Wild Card', 'W', 'L', 'GB', 'M#'],
        'body': [_w45, _w56, _w39, _w41]
    }]
}
