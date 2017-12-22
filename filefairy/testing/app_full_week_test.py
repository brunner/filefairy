#!/usr/bin/env python

import threading
import time

from app_test import AppTest
from slack_api import chat_post_message
from utils import assert_equals


inpt = ['07/19/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1913.html|Arizona 4, San Diego 1>*\n' +
        '*<https://game_box_1906.html|Boston 10, Minnesota 2>*\n' +
        '*<https://game_box_1910.html|Cincinnati 5, Pittsburgh 2>*\n' +
        '*<https://game_box_1914.html|Colorado 8, Atlanta 6>*\n' +
        '*<https://game_box_1909.html|Detroit 2, Los Angeles 1>*\n' +
        '*<https://game_box_1903.html|Houston 4, Seattle 0>*\n' +
        '*<https://game_box_1911.html|Los Angeles 8, San Francisco 1>*\n' +
        '*<https://game_box_1905.html|Milwaukee 3, Baltimore 2>*\n' +
        '*<https://game_box_1907.html|New York 5, Miami 1>*\n' +
        '*<https://game_box_1904.html|Oakland 7, Chicago 4>*\n' +
        '*<https://game_box_1912.html|Toronto 6, Kansas City 4>*\n' +
        '*<https://game_box_1908.html|Washington 5, Philadelphia 3>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/19/2021\n' +
        'Cincinnati Reds                64\nColorado Rockies               54\n' +
        'Minnesota Twins                53\nSan Diego Padres               52\n' +
        'New York Mets                  51\nLos Angeles Dodgers            51\n' +
        'Seattle Mariners               51\nToronto Blue Jays              51\n' +
        'Boston Red Sox                 49\nBaltimore Orioles              47\n' +
        'Atlanta Braves                 47\nKansas City Royals             45\n' +
        'Philadelphia Phillies          44\nChicago White Sox              44\n' +
        'Detroit Tigers                 43\nMilwaukee Brewers              41\n' +
        'Arizona Diamondbacks           41\nLos Angeles Angels             41\n' +
        'Houston Astros                 40\nWashington Nationals           39\n' +
        'San Francisco Giants           39\nOakland Athletics              39\n' +
        'Miami Marlins                  30\nPittsburgh Pirates             26```',
        '07/20/2021 LF <https://player_25233.html|Kyle Tucker> was injured ' +
        'on a defensive play (Texas @ Seattle)',
        '07/20/2021 SS <https://player_37609.html|Franklin Barreto> was injured ' +
        'while stealing a base (Atlanta @ Colorado)',
        '07/20/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1928.html|Arizona 9, San Diego 6>*\n' +
        '*<https://game_box_1916.html|Chicago 5, Oakland 3>*\n' +
        '*<https://game_box_1924.html|Cincinnati 4, Pittsburgh 3>*\n' +
        '*<https://game_box_1929.html|Colorado 5, Atlanta 3>*\n' +
        '*<https://game_box_1919.html|Houston 6, Cleveland 3>*\n' +
        '*<https://game_box_1922.html|Los Angeles 5, Detroit 3>*\n' +
        '*<https://game_box_1926.html|Los Angeles 5, San Francisco 0>*\n' +
        '*<https://game_box_1917.html|Milwaukee 6, Baltimore 2>*\n' +
        '*<https://game_box_1918.html|Minnesota 2, Boston 1>*\n' +
        '*<https://game_box_1920.html|New York 3, Miami 1>*\n' +
        '*<https://game_box_1915.html|Seattle 6, Texas 5>*\n' +
        '*<https://game_box_1923.html|St. Louis 6, Tampa Bay 4>*\n' +
        '*<https://game_box_1927.html|Toronto 5, Kansas City 0>*\n' +
        '*<https://game_box_1921.html|Washington 2, Philadelphia 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/20/2021\n' +
        'Cincinnati Reds                65\nColorado Rockies               55\n' +
        'Minnesota Twins                54\nNew York Mets                  52\n' +
        'Los Angeles Dodgers            52\nSan Diego Padres               52\n' +
        'Seattle Mariners               52\nToronto Blue Jays              52\n' +
        'Boston Red Sox                 49\nSt. Louis Cardinals            48\n' +
        'Atlanta Braves                 47\nTampa Bay Rays                 47\n' +
        'Baltimore Orioles              47\nKansas City Royals             45\n' +
        'Chicago White Sox              45\nCleveland Indians              45\n' +
        'Philadelphia Phillies          44\nDetroit Tigers                 43\n' +
        'Milwaukee Brewers              42\nLos Angeles Angels             42\n' +
        'Arizona Diamondbacks           42\nHouston Astros                 41\n' +
        'Washington Nationals           40\nSan Francisco Giants           39\n' +
        'Oakland Athletics              39\nMiami Marlins                  30\n' +
        'Texas Rangers                  30\nPittsburgh Pirates             26```',
        '07/21/2021 RP <https://player_37039.html|Lucas Sims> was injured ' +
        'while pitching (Texas @ Seattle)',
        '07/21/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1944.html|Arizona 5, San Diego 3>*\n' +
        '*<https://game_box_1932.html|Atlanta 7, Colorado 5>*\n' +
        '*<https://game_box_1935.html|Baltimore 4, Milwaukee 3>*\n' +
        '*<https://game_box_1936.html|Boston 5, Minnesota 3>*\n' +
        '*<https://game_box_1925.html|Chicago 5, New York 1>*\n' +
        '*<https://game_box_1934.html|Chicago 7, Oakland 2>*\n' +
        '*<https://game_box_1937.html|Cleveland 7, Houston 6>*\n' +
        '*<https://game_box_1939.html|Los Angeles 11, Detroit 9>*\n' +
        '*<https://game_box_1942.html|Los Angeles 2, San Francisco 0>*\n' +
        '*<https://game_box_1941.html|New York 4, Chicago 2>*\n' +
        '*<https://game_box_1938.html|New York 9, Miami 0>*\n' +
        '*<https://game_box_1930.html|Philadelphia 6, Washington 3>*\n' +
        '*<https://game_box_1931.html|Pittsburgh 6, Cincinnati 5>*\n' +
        '*<https://game_box_1933.html|Seattle 4, Texas 3>*\n' +
        '*<https://game_box_1940.html|Tampa Bay 6, St. Louis 4>*\n' +
        '*<https://game_box_1943.html|Toronto 5, Kansas City 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/21/2021\n' +
        'Cincinnati Reds                65\nColorado Rockies               55\n' +
        'Minnesota Twins                54\nLos Angeles Dodgers            53\n' +
        'Toronto Blue Jays              53\nNew York Mets                  53\n' +
        'Seattle Mariners               53\nSan Diego Padres               52\n' +
        'Boston Red Sox                 50\nBaltimore Orioles              48\n' +
        'Atlanta Braves                 48\nSt. Louis Cardinals            48\n' +
        'Tampa Bay Rays                 48\nChicago Cubs                   47\n' +
        'Chicago White Sox              46\nCleveland Indians              46\n' +
        'Kansas City Royals             45\nPhiladelphia Phillies          45\n' +
        'Arizona Diamondbacks           43\nDetroit Tigers                 43\n' +
        'Los Angeles Angels             43\nMilwaukee Brewers              42\n' +
        'New York Yankees               42\nHouston Astros                 41\n' +
        'Washington Nationals           40\nOakland Athletics              39\n' +
        'San Francisco Giants           39\nMiami Marlins                  30\n' +
        'Texas Rangers                  30\nPittsburgh Pirates             27```',
        '07/22/2021 <https://player_584.html|Brett Austin> ties the AL regular ' +
        'season extra-inning game record for runs with 4 (Oakland @ Chicago)',
        '07/22/2021 <https://player_36905.html|Jeffrey Baez> ties the CHC regular ' +
        'season extra-inning game record for strikeouts with 5 (Chicago @ St. Louis)',
        '07/22/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1948.html|Chicago 12, Oakland 11>*\n' +
        '*<https://game_box_1954.html|Cincinnati 3, San Francisco 2>*\n' +
        '*<https://game_box_1956.html|Colorado 7, Arizona 4>*\n' +
        '*<https://game_box_1946.html|Detroit 6, Los Angeles 2>*\n' +
        '*<https://game_box_1945.html|Houston 9, Cleveland 2>*\n' +
        '*<https://game_box_1955.html|Los Angeles 6, San Diego 1>*\n' +
        '*<https://game_box_1950.html|Minnesota 2, Boston 0>*\n' +
        '*<https://game_box_1951.html|New York 5, Miami 1>*\n' +
        '*<https://game_box_1947.html|Seattle 10, Texas 1>*\n' +
        '*<https://game_box_1953.html|St. Louis 6, Chicago 5>*\n' +
        '*<https://game_box_1949.html|Toronto 9, Kansas City 6>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/22/2021\n' +
        'Cincinnati Reds                66\nColorado Rockies               56\n' +
        'Minnesota Twins                55\nLos Angeles Dodgers            54\n' +
        'Toronto Blue Jays              54\nSeattle Mariners               54\n' +
        'New York Mets                  54\nSan Diego Padres               52\n' +
        'Boston Red Sox                 50\nSt. Louis Cardinals            49\n' +
        'Chicago Cubs                   47\nChicago White Sox              47\n' +
        'Cleveland Indians              46\nKansas City Royals             45\n' +
        'Detroit Tigers                 44\nLos Angeles Angels             43\n' +
        'Arizona Diamondbacks           43\nHouston Astros                 42\n' +
        'Oakland Athletics              39\nSan Francisco Giants           39\n' +
        'Miami Marlins                  30\nTexas Rangers                  30```',
        '07/23/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1970.html|Arizona 3, Colorado 0>*\n' +
        '*<https://game_box_1960.html|Atlanta 2, Milwaukee 1>*\n' +
        '*<https://game_box_1967.html|Baltimore 5, Kansas City 4>*\n' +
        '*<https://game_box_1966.html|Cincinnati 2, San Francisco 0>*\n' +
        '*<https://game_box_1958.html|Houston 4, Oakland 0>*\n' +
        '*<https://game_box_1959.html|Los Angeles 8, Chicago 5>*\n' +
        '*<https://game_box_1962.html|Minnesota 3, Cleveland 2>*\n' +
        '*<https://game_box_1957.html|New York 5, Texas 1>*\n' +
        '*<https://game_box_1963.html|New York 7, Detroit 4>*\n' +
        '*<https://game_box_1964.html|Philadelphia 6, Miami 2>*\n' +
        '*<https://game_box_1965.html|Pittsburgh 2, Washington 1>*\n' +
        '*<https://game_box_1969.html|San Diego 4, Los Angeles 3>*\n' +
        '*<https://game_box_1961.html|Seattle 10, Boston 3>*\n' +
        '*<https://game_box_1971.html|St. Louis 3, Chicago 2>*\n' +
        '*<https://game_box_1968.html|Tampa Bay 13, Toronto 10>*\n' +
        '*<https://game_box_1952.html|Washington 5, Pittsburgh 0>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/23/2021\n' +
        'Cincinnati Reds                67\nMinnesota Twins                56\n' +
        'Colorado Rockies               56\nNew York Mets                  55\n' +
        'Seattle Mariners               55\nLos Angeles Dodgers            54\n' +
        'Toronto Blue Jays              54\nSan Diego Padres               53\n' +
        'St. Louis Cardinals            50\nBoston Red Sox                 50\n' +
        'Atlanta Braves                 49\nBaltimore Orioles              49\n' +
        'Tampa Bay Rays                 49\nChicago White Sox              47\n' +
        'Chicago Cubs                   47\nPhiladelphia Phillies          46\n' +
        'Cleveland Indians              46\nKansas City Royals             45\n' +
        'Arizona Diamondbacks           44\nLos Angeles Angels             44\n' +
        'Detroit Tigers                 44\nHouston Astros                 43\n' +
        'New York Yankees               43\nMilwaukee Brewers              42\n' +
        'Washington Nationals           41\nSan Francisco Giants           39\n' +
        'Oakland Athletics              39\nTexas Rangers                  30\n' +
        'Miami Marlins                  30\nPittsburgh Pirates             28```',
        '07/24/2021 3B <https://player_22458.html|Alex Bregman> was injured ' +
        'while running the bases (San Diego @ Los Angeles)',
        '07/24/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1972.html|Chicago 11, Los Angeles 2>*\n' +
        '*<https://game_box_1986.html|Colorado 4, Arizona 1>*\n' +
        '*<https://game_box_1976.html|Detroit 8, New York 5>*\n' +
        '*<https://game_box_1977.html|Houston 9, Oakland 8>*\n' +
        '*<https://game_box_1983.html|Kansas City 12, Baltimore 4>*\n' +
        '*<https://game_box_1978.html|Los Angeles 2, San Diego 1>*\n' +
        '*<https://game_box_1979.html|Milwaukee 3, Atlanta 2>*\n' +
        '*<https://game_box_1975.html|Minnesota 7, Cleveland 5>*\n' +
        '*<https://game_box_1973.html|New York 4, Texas 1>*\n' +
        '*<https://game_box_1985.html|San Francisco 4, Cincinnati 2>*\n' +
        '*<https://game_box_1981.html|Seattle 2, Boston 0>*\n' +
        '*<https://game_box_1980.html|St. Louis 11, Chicago 6>*\n' +
        '*<https://game_box_1984.html|Tampa Bay 9, Toronto 5>*\n' +
        '*<https://game_box_1974.html|Washington 5, Pittsburgh 2>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/24/2021\n' +
        'Cincinnati Reds                67\nColorado Rockies               57\n' +
        'Minnesota Twins                57\nNew York Mets                  56\n' +
        'Seattle Mariners               56\nLos Angeles Dodgers            55\n' +
        'Toronto Blue Jays              54\nSan Diego Padres               53\n' +
        'St. Louis Cardinals            51\nTampa Bay Rays                 50\n' +
        'Boston Red Sox                 50\nAtlanta Braves                 49\n' +
        'Baltimore Orioles              49\nChicago White Sox              48\n' +
        'Chicago Cubs                   47\nCleveland Indians              46\n' +
        'Kansas City Royals             46\nDetroit Tigers                 45\n' +
        'Houston Astros                 44\nLos Angeles Angels             44\n' +
        'Arizona Diamondbacks           44\nMilwaukee Brewers              43\n' +
        'New York Yankees               43\nWashington Nationals           42\n' +
        'San Francisco Giants           40\nOakland Athletics              39\n' +
        'Texas Rangers                  30\nPittsburgh Pirates             28```',
        '07/25/2021 <https://player_29845.html|Michael Massey> ties the AL regular ' +
        'season extra-inning game record for doubles with 3 (New York @ Detroit)',
        '07/25/2021 <https://player_29845.html|Michael Massey> ties the AL regular ' +
        'season extra-inning game record for hits with 5 (New York @ Detroit)',
        '07/25/2021 <https://player_29845.html|Michael Massey> sets the AL regular ' +
        'season extra-inning game record for doubles with 4 (New York @ Detroit)',
        '07/25/2021 MAJOR LEAGUE BASEBALL Final Scores\n' +
        '*<https://game_box_1993.html|Atlanta 4, Milwaukee 3>*\n' +
        '*<https://game_box_1989.html|Boston 7, Seattle 1>*\n' +
        '*<https://game_box_1988.html|Chicago 6, Los Angeles 5>*\n' +
        '*<https://game_box_1994.html|Cleveland 7, Minnesota 2>*\n' +
        '*<https://game_box_2000.html|Colorado 8, Arizona 1>*\n' +
        '*<https://game_box_1996.html|Kansas City 10, Baltimore 3>*\n' +
        '*<https://game_box_1998.html|Los Angeles 6, San Diego 0>*\n' +
        '*<https://game_box_1982.html|Miami 11, Philadelphia 2>*\n' +
        '*<https://game_box_1991.html|New York 10, Texas 1>*\n' +
        '*<https://game_box_1995.html|New York 3, Detroit 2>*\n' +
        '*<https://game_box_1987.html|Oakland 5, Houston 3>*\n' +
        '*<https://game_box_1990.html|Philadelphia 9, Miami 4>*\n' +
        '*<https://game_box_1992.html|Pittsburgh 12, Washington 8>*\n' +
        '*<https://game_box_1999.html|San Francisco 4, Cincinnati 3>*\n' +
        '*<https://game_box_2001.html|St. Louis 4, Chicago 1>*\n' +
        '*<https://game_box_1997.html|Toronto 10, Tampa Bay 1>*',
        '```MAJOR LEAGUE BASEBALL Live Table - 07/25/2021\n' +
        'Cincinnati Reds                67\nColorado Rockies               58\n' +
        'New York Mets                  57\nMinnesota Twins                57\n' +
        'Seattle Mariners               56\nLos Angeles Dodgers            56\n' +
        'Toronto Blue Jays              55\nSan Diego Padres               53\n' +
        'St. Louis Cardinals            52\nBoston Red Sox                 51\n' +
        'Atlanta Braves                 50\nTampa Bay Rays                 50\n' +
        'Chicago White Sox              49\nBaltimore Orioles              49\n' +
        'Philadelphia Phillies          47\nCleveland Indians              47\n' +
        'Chicago Cubs                   47\nKansas City Royals             47\n' +
        'Detroit Tigers                 45\nArizona Diamondbacks           44\n' +
        'New York Yankees               44\nHouston Astros                 44\n' +
        'Los Angeles Angels             44\nMilwaukee Brewers              43\n' +
        'Washington Nationals           42\nSan Francisco Giants           41\n' +
        'Oakland Athletics              40\nMiami Marlins                  31\n' +
        'Texas Rangers                  30\nPittsburgh Pirates             29```']

outpt = '07/19/2021\n' + \
        '<https://game_box_1913.html|Arizona 4, San Diego 1>\n' + \
        '<https://game_box_1906.html|Boston 10, Minnesota 2>\n' + \
        '<https://game_box_1910.html|Cincinnati 5, Pittsburgh 2>\n' + \
        '<https://game_box_1914.html|Colorado 8, Atlanta 6>\n' + \
        '<https://game_box_1909.html|Detroit 2, Los Angeles 1>\n' + \
        '<https://game_box_1903.html|Houston 4, Seattle 0>\n' + \
        '<https://game_box_1911.html|Los Angeles 8, San Francisco 1>\n' + \
        '<https://game_box_1905.html|Milwaukee 3, Baltimore 2>\n' + \
        '<https://game_box_1907.html|New York 5, Miami 1>\n' + \
        '<https://game_box_1904.html|Oakland 7, Chicago 4>\n' + \
        '<https://game_box_1912.html|Toronto 6, Kansas City 4>\n' + \
        '<https://game_box_1908.html|Washington 5, Philadelphia 3>\n' + \
        '07/20/2021\n' + \
        '<https://game_box_1928.html|Arizona 9, San Diego 6>\n' + \
        '<https://game_box_1916.html|Chicago 5, Oakland 3>\n' + \
        '<https://game_box_1924.html|Cincinnati 4, Pittsburgh 3>\n' + \
        '<https://game_box_1929.html|Colorado 5, Atlanta 3>\n' + \
        '<https://game_box_1919.html|Houston 6, Cleveland 3>\n' + \
        '<https://game_box_1922.html|Los Angeles 5, Detroit 3>\n' + \
        '<https://game_box_1926.html|Los Angeles 5, San Francisco 0>\n' + \
        '<https://game_box_1917.html|Milwaukee 6, Baltimore 2>\n' + \
        '<https://game_box_1918.html|Minnesota 2, Boston 1>\n' + \
        '<https://game_box_1920.html|New York 3, Miami 1>\n' + \
        '<https://game_box_1915.html|Seattle 6, Texas 5>\n' + \
        '<https://game_box_1923.html|St. Louis 6, Tampa Bay 4>\n' + \
        '<https://game_box_1927.html|Toronto 5, Kansas City 0>\n' + \
        '<https://game_box_1921.html|Washington 2, Philadelphia 1>\n' + \
        '07/21/2021\n' + \
        '<https://game_box_1944.html|Arizona 5, San Diego 3>\n' + \
        '<https://game_box_1932.html|Atlanta 7, Colorado 5>\n' + \
        '<https://game_box_1935.html|Baltimore 4, Milwaukee 3>\n' + \
        '<https://game_box_1936.html|Boston 5, Minnesota 3>\n' + \
        '<https://game_box_1925.html|Chicago 5, New York 1>\n' + \
        '<https://game_box_1934.html|Chicago 7, Oakland 2>\n' + \
        '<https://game_box_1937.html|Cleveland 7, Houston 6>\n' + \
        '<https://game_box_1939.html|Los Angeles 11, Detroit 9>\n' + \
        '<https://game_box_1942.html|Los Angeles 2, San Francisco 0>\n' + \
        '<https://game_box_1941.html|New York 4, Chicago 2>\n' + \
        '<https://game_box_1938.html|New York 9, Miami 0>\n' + \
        '<https://game_box_1930.html|Philadelphia 6, Washington 3>\n' + \
        '<https://game_box_1931.html|Pittsburgh 6, Cincinnati 5>\n' + \
        '<https://game_box_1933.html|Seattle 4, Texas 3>\n' + \
        '<https://game_box_1940.html|Tampa Bay 6, St. Louis 4>\n' + \
        '<https://game_box_1943.html|Toronto 5, Kansas City 2>\n' + \
        '07/22/2021\n' + \
        '<https://game_box_1948.html|Chicago 12, Oakland 11>\n' + \
        '<https://game_box_1954.html|Cincinnati 3, San Francisco 2>\n' + \
        '<https://game_box_1956.html|Colorado 7, Arizona 4>\n' + \
        '<https://game_box_1946.html|Detroit 6, Los Angeles 2>\n' + \
        '<https://game_box_1945.html|Houston 9, Cleveland 2>\n' + \
        '<https://game_box_1955.html|Los Angeles 6, San Diego 1>\n' + \
        '<https://game_box_1950.html|Minnesota 2, Boston 0>\n' + \
        '<https://game_box_1951.html|New York 5, Miami 1>\n' + \
        '<https://game_box_1947.html|Seattle 10, Texas 1>\n' + \
        '<https://game_box_1953.html|St. Louis 6, Chicago 5>\n' + \
        '<https://game_box_1949.html|Toronto 9, Kansas City 6>\n' + \
        '07/23/2021\n' + \
        '<https://game_box_1970.html|Arizona 3, Colorado 0>\n' + \
        '<https://game_box_1960.html|Atlanta 2, Milwaukee 1>\n' + \
        '<https://game_box_1967.html|Baltimore 5, Kansas City 4>\n' + \
        '<https://game_box_1966.html|Cincinnati 2, San Francisco 0>\n' + \
        '<https://game_box_1958.html|Houston 4, Oakland 0>\n' + \
        '<https://game_box_1959.html|Los Angeles 8, Chicago 5>\n' + \
        '<https://game_box_1962.html|Minnesota 3, Cleveland 2>\n' + \
        '<https://game_box_1957.html|New York 5, Texas 1>\n' + \
        '<https://game_box_1963.html|New York 7, Detroit 4>\n' + \
        '<https://game_box_1964.html|Philadelphia 6, Miami 2>\n' + \
        '<https://game_box_1965.html|Pittsburgh 2, Washington 1>\n' + \
        '<https://game_box_1969.html|San Diego 4, Los Angeles 3>\n' + \
        '<https://game_box_1961.html|Seattle 10, Boston 3>\n' + \
        '<https://game_box_1971.html|St. Louis 3, Chicago 2>\n' + \
        '<https://game_box_1968.html|Tampa Bay 13, Toronto 10>\n' + \
        '<https://game_box_1952.html|Washington 5, Pittsburgh 0>\n' + \
        '07/24/2021\n' + \
        '<https://game_box_1972.html|Chicago 11, Los Angeles 2>\n' + \
        '<https://game_box_1986.html|Colorado 4, Arizona 1>\n' + \
        '<https://game_box_1976.html|Detroit 8, New York 5>\n' + \
        '<https://game_box_1977.html|Houston 9, Oakland 8>\n' + \
        '<https://game_box_1983.html|Kansas City 12, Baltimore 4>\n' + \
        '<https://game_box_1978.html|Los Angeles 2, San Diego 1>\n' + \
        '<https://game_box_1979.html|Milwaukee 3, Atlanta 2>\n' + \
        '<https://game_box_1975.html|Minnesota 7, Cleveland 5>\n' + \
        '<https://game_box_1973.html|New York 4, Texas 1>\n' + \
        '<https://game_box_1985.html|San Francisco 4, Cincinnati 2>\n' + \
        '<https://game_box_1981.html|Seattle 2, Boston 0>\n' + \
        '<https://game_box_1980.html|St. Louis 11, Chicago 6>\n' + \
        '<https://game_box_1984.html|Tampa Bay 9, Toronto 5>\n' + \
        '<https://game_box_1974.html|Washington 5, Pittsburgh 2>\n' + \
        '07/25/2021\n' + \
        '<https://game_box_1993.html|Atlanta 4, Milwaukee 3>\n' + \
        '<https://game_box_1989.html|Boston 7, Seattle 1>\n' + \
        '<https://game_box_1988.html|Chicago 6, Los Angeles 5>\n' + \
        '<https://game_box_1994.html|Cleveland 7, Minnesota 2>\n' + \
        '<https://game_box_2000.html|Colorado 8, Arizona 1>\n' + \
        '<https://game_box_1996.html|Kansas City 10, Baltimore 3>\n' + \
        '<https://game_box_1998.html|Los Angeles 6, San Diego 0>\n' + \
        '<https://game_box_1982.html|Miami 11, Philadelphia 2>\n' + \
        '<https://game_box_1991.html|New York 10, Texas 1>\n' + \
        '<https://game_box_1995.html|New York 3, Detroit 2>\n' + \
        '<https://game_box_1987.html|Oakland 5, Houston 3>\n' + \
        '<https://game_box_1990.html|Philadelphia 9, Miami 4>\n' + \
        '<https://game_box_1992.html|Pittsburgh 12, Washington 8>\n' + \
        '<https://game_box_1999.html|San Francisco 4, Cincinnati 3>\n' + \
        '<https://game_box_2001.html|St. Louis 4, Chicago 1>\n' + \
        '<https://game_box_1997.html|Toronto 10, Tampa Bay 1>'

injrs = 'Injuries:\n' + \
        '<https://player_25233.html|Kyle Tucker> (defensive play)\n' + \
        '<https://player_37609.html|Franklin Barreto> (stealing a base)\n' + \
        '<https://player_37039.html|Lucas Sims> (pitching)\n' + \
        '<https://player_22458.html|Alex Bregman> (running the bases)'

rcrds = 'AL East\n' + \
        ':jays: 5-2 :separator: :yankees: 3-2 :separator: :rays: 3-2 ' + \
        ':separator: :redsox: 3-4 :separator: :orioles: 2-4\n\n' + \
        'AL Central\n' + \
        ':whitesox: 5-2 :separator: :twincities: 4-3 :separator: :crackeyes: 3-4 ' + \
        ':separator: :indians: 2-4 :separator: :monarchs: 2-5\n\n' + \
        'AL West\n' + \
        ':stros: 5-2 :separator: :mariners: 5-2 :separator: :angels: 3-4 ' + \
        ':separator: :athletics: 2-5 :separator: :rangers: 0-6\n\n' + \
        'NL East\n' + \
        ':mets: 7-0 :separator: :nationals: 4-3 :separator: :braves: 3-3 ' + \
        ':separator: :phillies: 3-3 :separator: :marlins: 1-6\n\n' + \
        'NL Central\n' + \
        ':cardinals: 5-1 :separator: :reds: 4-3 :separator: :brewers: 3-3 ' + \
        ':separator: :pirates: 3-4 :separator: :cubbies: 1-5\n\n' + \
        'NL West\n' + \
        ':dodgers: 6-1 :separator: :rox: 5-2 :separator: :dbacks: 4-3 ' + \
        ':separator: :giants: 2-5 :separator: :pads: 1-6'

stnds = 'AL East         |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Toronto         |  55 |  40 |     - |  64\n' + \
        'Boston          |  51 |  44 |   4.0 |    \n' + \
        'Tampa Bay       |  50 |  44 |   4.5 |    \n' + \
        'Baltimore       |  49 |  46 |   6.0 |    \n' + \
        'New York        |  44 |  50 |  10.5 |    \n\n' + \
        'AL Central      |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Minnesota       |  57 |  39 |     - |  59\n' + \
        'Chicago         |  49 |  47 |   8.0 |    \n' + \
        'Cleveland       |  47 |  49 |  10.0 |    \n' + \
        'Kansas City     |  47 |  50 |  10.5 |    \n' + \
        'Detroit         |  45 |  51 |  12.0 |    \n\n' + \
        'AL West         |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Seattle         |  56 |  39 |     - |  56\n' + \
        'Houston         |  44 |  51 |  12.0 |    \n' + \
        'Los Angeles     |  44 |  51 |  12.0 |    \n' + \
        'Oakland         |  40 |  54 |  15.5 |    \n' + \
        'Texas           |  30 |  64 |  25.5 |    \n\n' + \
        'AL Wild Card    |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Boston          |  51 |  44 |  +0.5 |  66\n' + \
        'Tampa Bay       |  50 |  44 |     - |  67\n' + \
        'Baltimore       |  49 |  46 |   1.5 |    \n' + \
        'Chicago         |  49 |  47 |   2.0 |    \n' + \
        'Cleveland       |  47 |  49 |   4.0 |    \n' + \
        'Kansas City     |  47 |  50 |   4.5 |    \n' + \
        'Detroit         |  45 |  51 |   6.0 |    \n' + \
        'New York        |  44 |  50 |   6.0 |    \n' + \
        'Houston         |  44 |  51 |   6.5 |    \n' + \
        'Los Angeles     |  44 |  51 |   6.5 |    \n' + \
        'Oakland         |  40 |  54 |  10.0 |    \n' + \
        'Texas           |  30 |  64 |  20.0 |    \n' + \
        'NL East         |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'New York        |  57 |  39 |     - |  62\n' + \
        'Atlanta         |  50 |  44 |   6.0 |    \n' + \
        'Philadelphia    |  47 |  47 |   9.0 |    \n' + \
        'Washington      |  42 |  53 |  14.5 |    \n' + \
        'Miami           |  31 |  65 |  26.0 |    \n\n' + \
        'NL Central      |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Cincinnati      |  67 |  28 |     - |  55\n' + \
        'St. Louis       |  52 |  41 |  14.0 |    \n' + \
        'Chicago         |  47 |  47 |  19.5 |    \n' + \
        'Milwaukee       |  43 |  51 |  23.5 |    \n' + \
        'Pittsburgh      |  29 |  67 |  38.5 |    \n\n' + \
        'NL West         |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Colorado        |  58 |  37 |     - |  67\n' + \
        'Los Angeles     |  56 |  38 |   1.5 |    \n' + \
        'San Diego       |  53 |  42 |   5.0 |    \n' + \
        'Arizona         |  44 |  52 |  14.5 |    \n' + \
        'San Francisco   |  41 |  55 |  17.5 |    \n\n' + \
        'NL Wild Card    |   W |   L |    GB |  M#\n' + \
        '----------------|-----|-----|-------|-----\n' + \
        'Los Angeles     |  56 |  38 |  +3.5 |  65\n' + \
        'St. Louis       |  52 |  41 |     - |  69\n' + \
        'San Diego       |  53 |  42 |     - |  69\n' + \
        'Atlanta         |  50 |  44 |   2.5 |    \n' + \
        'Chicago         |  47 |  47 |   5.5 |    \n' + \
        'Philadelphia    |  47 |  47 |   5.5 |    \n' + \
        'Arizona         |  44 |  52 |   9.5 |    \n' + \
        'Milwaukee       |  43 |  51 |   9.5 |    \n' + \
        'Washington      |  42 |  53 |  11.0 |    \n' + \
        'San Francisco   |  41 |  55 |  12.5 |    \n' + \
        'Miami           |  31 |  65 |  22.5 |    \n' + \
        'Pittsburgh      |  29 |  67 |  24.5 |    '


def test():
  appTest = AppTest(settings_in='data/settings_in.txt', standings_in='data/standings_full_week.txt')
  appTest.setup()

  t1 = threading.Thread(target=appTest.listen)
  t1.start()
  time.sleep(6)

  for i in inpt:
    chat_post_message('testing', i)
  time.sleep(2)

  assert_equals(appTest.process_final_scores(), outpt)
  assert_equals(appTest.process_injuries(), injrs)
  assert_equals(appTest.process_records(), rcrds)
  assert_equals(appTest.process_standings(), stnds)

  appTest.handle_close()
  t1.join()

  with open(appTest.get_standings_out(), 'r') as fo:
    with open(appTest.get_path() + 'data/standings_full_week_gold.txt', 'r') as fg:
      assert_equals(fo.read(), fg.read())


if __name__ == '__main__':
  test()
