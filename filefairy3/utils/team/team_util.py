#!/usr/bin/env python
# -*- coding: utf-8 -*-

_collection = {
    '31': 'Arizona Diamondbacks',
    '32': 'Atlanta Braves',
    '33': 'Baltimore Orioles',
    '34': 'Boston Red Sox',
    '35': 'Chicago White Sox',
    '36': 'Chicago Cubs',
    '37': 'Cincinnati Reds',
    '38': 'Cleveland Indians',
    '39': 'Colorado Rockies',
    '40': 'Detroit Tigers',
    '41': 'Miami Marlins',
    '42': 'Houston Astros',
    '43': 'Kansas City Royals',
    '44': 'Los Angeles Angels',
    '45': 'Los Angeles Dodgers',
    '46': 'Milwaukee Brewers',
    '47': 'Minnesota Twins',
    '48': 'New York Yankees',
    '49': 'New York Mets',
    '50': 'Oakland Athletics',
    '51': 'Philadelphia Phillies',
    '52': 'Pittsburgh Pirates',
    '53': 'San Diego Padres',
    '54': 'Seattle Mariners',
    '55': 'San Francisco Giants',
    '56': 'St. Louis Cardinals',
    '57': 'Tampa Bay Rays',
    '58': 'Texas Rangers',
    '59': 'Toronto Blue Jays',
    '60': 'Washington Nationals',
}


def full_name(teamid):
    return _collection.get(teamid, '')
