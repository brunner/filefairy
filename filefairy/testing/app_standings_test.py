#!/usr/bin/env python

from app_test import AppTest
from utils import assert_equals

inpt = ['data/standings_august.txt',
        'data/standings_baddivision.txt',
        'data/standings_final.txt',
        'data/standings_irregular.txt',
        'data/standings_linear.txt',
        'data/standings_opening_day.txt',
        'data/standings_today.txt']


outp = ['AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Toronto         |  64 |  47 |     - |  45\n' +
        'Baltimore       |  57 |  54 |   7.0 |    \n' +
        'Tampa Bay       |  57 |  54 |   7.0 |    \n' +
        'Boston          |  55 |  55 |   8.5 |    \n' +
        'New York        |  50 |  60 |  13.5 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Minnesota       |  66 |  45 |     - |  44\n' +
        'Cleveland       |  59 |  53 |   7.5 |    \n' +
        'Chicago         |  57 |  54 |   9.0 |    \n' +
        'Kansas City     |  54 |  59 |  13.0 |    \n' +
        'Detroit         |  53 |  58 |  13.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Seattle         |  65 |  45 |     - |  44\n' +
        'Houston         |  54 |  57 |  11.5 |    \n' +
        'Los Angeles     |  53 |  58 |  12.5 |    \n' +
        'Oakland         |  46 |  54 |  14.0 |    \n' +
        'Texas           |  37 |  74 |  28.5 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cleveland       |  59 |  53 |  +1.5 |  50\n' +
        'Baltimore       |  57 |  54 |     - |  52\n' +
        'Chicago         |  57 |  54 |     - |  52\n' +
        'Tampa Bay       |  57 |  54 |     - |  52\n' +
        'Boston          |  55 |  55 |   1.5 |    \n' +
        'Houston         |  54 |  57 |   3.0 |    \n' +
        'Kansas City     |  54 |  59 |   4.0 |    \n' +
        'Detroit         |  53 |  58 |   4.0 |    \n' +
        'Los Angeles     |  53 |  58 |   4.0 |    \n' +
        'Oakland         |  46 |  54 |   5.5 |    \n' +
        'New York        |  50 |  60 |   6.5 |    \n' +
        'Texas           |  37 |  74 |  20.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'New York        |  64 |  47 |     - |  45\n' +
        'Philadelphia    |  57 |  54 |   7.0 |    \n' +
        'Atlanta         |  56 |  55 |   8.0 |    \n' +
        'Washington      |  49 |  63 |  15.5 |    \n' +
        'Miami           |  36 |  75 |  28.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |  77 |  34 |     - |  34\n' +
        'St. Louis       |  59 |  52 |  18.0 |    \n' +
        'Chicago         |  57 |  53 |  19.5 |    \n' +
        'Milwaukee       |  52 |  59 |  25.0 |    \n' +
        'Pittsburgh      |  34 |  78 |  43.5 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  69 |  41 |     - |  48\n' +
        'San Diego       |  67 |  46 |   3.5 |    \n' +
        'Los Angeles     |  63 |  46 |   5.5 |    \n' +
        'Arizona         |  50 |  62 |  20.0 |    \n' +
        'San Francisco   |  48 |  63 |  21.5 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'San Diego       |  67 |  46 |  +2.0 |  44\n' +
        'Los Angeles     |  63 |  46 |     - |  48\n' +
        'St. Louis       |  59 |  52 |   5.0 |    \n' +
        'Chicago         |  57 |  53 |   6.5 |    \n' +
        'Philadelphia    |  57 |  54 |   7.0 |    \n' +
        'Atlanta         |  56 |  55 |   8.0 |    \n' +
        'Milwaukee       |  52 |  59 |  12.0 |    \n' +
        'Arizona         |  50 |  62 |  14.5 |    \n' +
        'Washington      |  49 |  63 |  15.5 |    \n' +
        'San Francisco   |  48 |  63 |  16.0 |    \n' +
        'Miami           |  36 |  75 |  28.0 |    \n' +
        'Pittsburgh      |  34 |  78 |  30.5 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Toronto         |  80 |  55 |     - |  19\n' +
        'Boston          |  70 |  64 |   9.5 |    \n' +
        'New York        |  65 |  70 |  15.0 |    \n' +
        'Tampa Bay       |  65 |  71 |  15.5 |    \n' +
        'Baltimore       |  53 |  82 |  27.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cleveland       |  84 |  52 |     - |  19\n' +
        'Detroit         |  75 |  60 |   8.5 |    \n' +
        'Minnesota       |  75 |  61 |   9.0 |    \n' +
        'Chicago         |  65 |  70 |  18.5 |    \n' +
        'e-Kansas City   |  48 |  89 |  36.5 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Houston         |  70 |  65 |     - |  27\n' +
        'Los Angeles     |  71 |  66 |     - |  27\n' +
        'Seattle         |  67 |  70 |   4.0 |    \n' +
        'Oakland         |  65 |  72 |   6.0 |    \n' +
        'Texas           |  61 |  75 |   9.5 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Detroit         |  75 |  60 |  +0.5 |  24\n' +
        'Minnesota       |  75 |  61 |     - |  24\n' +
        'Boston          |  70 |  64 |   4.0 |    \n' +
        'Houston         |  70 |  65 |   4.5 |    \n' +
        'Los Angeles     |  71 |  66 |   4.5 |    \n' +
        'Seattle         |  67 |  70 |   8.5 |    \n' +
        'Chicago         |  65 |  70 |   9.5 |    \n' +
        'New York        |  65 |  70 |   9.5 |    \n' +
        'Tampa Bay       |  65 |  71 |  10.0 |    \n' +
        'Oakland         |  65 |  72 |  10.5 |    \n' +
        'Texas           |  61 |  75 |  14.0 |    \n' +
        'Baltimore       |  53 |  82 |  21.5 |    \n' +
        'e-Kansas City   |  48 |  89 |  27.5 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Miami           |  80 |  57 |     - |  13\n' +
        'Washington      |  67 |  70 |  13.0 |    \n' +
        'Philadelphia    |  64 |  72 |  15.5 |    \n' +
        'New York        |  59 |  78 |  21.0 |    \n' +
        'Atlanta         |  58 |  79 |  22.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Chicago         |  82 |  53 |     - |  24\n' +
        'Milwaukee       |  79 |  57 |   3.5 |    \n' +
        'Pittsburgh      |  74 |  62 |   8.5 |    \n' +
        'Cincinnati      |  60 |  76 |  22.5 |    \n' +
        'St. Louis       |  60 |  77 |  23.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Los Angeles     |  89 |  47 |     - |  14\n' +
        'Arizona         |  77 |  60 |  12.5 |    \n' +
        'San Diego       |  63 |  75 |  27.0 |    \n' +
        'Colorado        |  61 |  75 |  28.0 |    \n' +
        'San Francisco   |  55 |  82 |  34.5 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Milwaukee       |  79 |  57 |  +2.5 |  22\n' +
        'Arizona         |  77 |  60 |     - |  24\n' +
        'Pittsburgh      |  74 |  62 |   2.5 |    \n' +
        'Washington      |  67 |  70 |  10.0 |    \n' +
        'Philadelphia    |  64 |  72 |  12.5 |    \n' +
        'San Diego       |  63 |  75 |  14.5 |    \n' +
        'Colorado        |  61 |  75 |  15.5 |    \n' +
        'Cincinnati      |  60 |  76 |  16.5 |    \n' +
        'St. Louis       |  60 |  77 |  17.0 |    \n' +
        'New York        |  59 |  78 |  18.0 |    \n' +
        'Atlanta         |  58 |  79 |  19.0 |    \n' +
        'San Francisco   |  55 |  82 |  22.0 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-Toronto       | 102 |  60 |     - |   X\n' +
        'z-Tampa Bay     |  86 |  76 |  16.0 |    \n' +
        'e-New York      |  78 |  84 |  24.0 |    \n' +
        'e-Boston        |  77 |  85 |  25.0 |    \n' +
        'e-Baltimore     |  74 |  88 |  28.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-Minnesota     |  88 |  74 |     - |   X\n' +
        'e-Chicago       |  84 |  78 |   4.0 |    \n' +
        'e-Kansas City   |  79 |  82 |   8.5 |    \n' +
        'e-Detroit       |  73 |  88 |  14.5 |    \n' +
        'e-Cleveland     |  65 |  97 |  23.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-Seattle       |  97 |  65 |     - |   X\n' +
        'z-Houston       |  87 |  75 |  10.0 |    \n' +
        'e-Los Angeles   |  85 |  77 |  12.0 |    \n' +
        'e-Oakland       |  71 |  90 |  25.5 |    \n' +
        'e-Texas         |  66 |  96 |  31.0 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'z-Houston       |  87 |  75 |  +1.0 |   X\n' +
        'z-Tampa Bay     |  86 |  76 |     - |   X\n' +
        'e-Los Angeles   |  85 |  77 |   1.0 |    \n' +
        'e-Chicago       |  84 |  78 |   2.0 |    \n' +
        'e-Kansas City   |  79 |  82 |   6.5 |    \n' +
        'e-New York      |  78 |  84 |   8.0 |    \n' +
        'e-Boston        |  77 |  85 |   9.0 |    \n' +
        'e-Baltimore     |  74 |  88 |  12.0 |    \n' +
        'e-Detroit       |  73 |  88 |  12.5 |    \n' +
        'e-Oakland       |  71 |  90 |  14.5 |    \n' +
        'e-Texas         |  66 |  96 |  20.0 |    \n' +
        'e-Cleveland     |  65 |  97 |  21.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-Philadelphia  |  99 |  63 |     - |   X\n' +
        'z-Atlanta       |  87 |  75 |  12.0 |    \n' +
        'e-New York      |  82 |  80 |  17.0 |    \n' +
        'e-Miami         |  74 |  88 |  25.0 |    \n' +
        'e-Washington    |  70 |  92 |  29.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-St. Louis     |  88 |  74 |     - |   X\n' +
        'e-Pittsburgh    |  84 |  78 |   4.0 |    \n' +
        'e-Milwaukee     |  78 |  84 |  10.0 |    \n' +
        'e-Chicago       |  73 |  89 |  15.0 |    \n' +
        'e-Cincinnati    |  69 |  93 |  19.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'x-San Francisco |  90 |  72 |     - |   X\n' +
        'z-Los Angeles   |  86 |  76 |   4.0 |    \n' +
        'e-Colorado      |  81 |  81 |   9.0 |    \n' +
        'e-Arizona       |  80 |  82 |  10.0 |    \n' +
        'e-San Diego     |  76 |  86 |  14.0 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'z-Atlanta       |  87 |  75 |  +1.0 |   X\n' +
        'z-Los Angeles   |  86 |  76 |     - |   X\n' +
        'e-Pittsburgh    |  84 |  78 |   2.0 |    \n' +
        'e-New York      |  82 |  80 |   4.0 |    \n' +
        'e-Colorado      |  81 |  81 |   5.0 |    \n' +
        'e-Arizona       |  80 |  82 |   6.0 |    \n' +
        'e-Milwaukee     |  78 |  84 |   8.0 |    \n' +
        'e-San Diego     |  76 |  86 |  10.0 |    \n' +
        'e-Miami         |  74 |  88 |  12.0 |    \n' +
        'e-Chicago       |  73 |  89 |  13.0 |    \n' +
        'e-Washington    |  70 |  92 |  16.0 |    \n' +
        'e-Cincinnati    |  69 |  93 |  17.0 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Baltimore       |  26 |  15 |     - | 124\n' +
        'Boston          |  23 |  13 |   0.5 |    \n' +
        'New York        |  17 |  20 |   7.0 |    \n' +
        'Tampa Bay       |  16 |  21 |   8.0 |    \n' +
        'Toronto         |  13 |  26 |  12.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cleveland       |  23 |  15 |     - | 124\n' +
        'Chicago         |  24 |  16 |     - | 124\n' +
        'Detroit         |  22 |  17 |   1.5 |    \n' +
        'Kansas City     |  13 |  26 |  10.5 |    \n' +
        'Minnesota       |  10 |  32 |  15.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Houston         |  25 |  13 |     - | 120\n' +
        'Los Angeles     |  21 |  18 |   4.5 |    \n' +
        'Oakland         |  19 |  19 |   6.0 |    \n' +
        'Seattle         |  17 |  20 |   7.5 |    \n' +
        'Texas           |  14 |  24 |  11.0 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Boston          |  23 |  13 |  +1.0 | 123\n' +
        'Cleveland       |  23 |  15 |     - | 123\n' +
        'Chicago         |  24 |  16 |     - | 122\n' +
        'Detroit         |  22 |  17 |   1.5 |    \n' +
        'Los Angeles     |  21 |  18 |   2.5 |    \n' +
        'Oakland         |  19 |  19 |   4.0 |    \n' +
        'New York        |  17 |  20 |   5.5 |    \n' +
        'Seattle         |  17 |  20 |   5.5 |    \n' +
        'Tampa Bay       |  16 |  21 |   6.5 |    \n' +
        'Texas           |  14 |  24 |   9.0 |    \n' +
        'Kansas City     |  13 |  26 |  10.5 |    \n' +
        'Toronto         |  13 |  26 |  10.5 |    \n' +
        'Minnesota       |  10 |  32 |  15.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Atlanta         |  25 |  12 |     - | 121\n' +
        'Miami           |  21 |  17 |   4.5 |    \n' +
        'New York        |  18 |  19 |   7.0 |    \n' +
        'Philadelphia    |  17 |  22 |   9.0 |    \n' +
        'Washington      |  14 |  26 |  12.5 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |  22 |  17 |     - | 123\n' +
        'Chicago         |  23 |  18 |     - | 123\n' +
        'Milwaukee       |  20 |  20 |   2.5 |    \n' +
        'Pittsburgh      |  16 |  19 |   4.0 |    \n' +
        'St. Louis       |  13 |  25 |   8.5 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  23 |  15 |     - | 124\n' +
        'Los Angeles     |  22 |  16 |   1.0 |    \n' +
        'Arizona         |  24 |  18 |   1.0 |    \n' +
        'San Diego       |  20 |  23 |   5.5 |    \n' +
        'San Francisco   |  16 |  26 |   9.0 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Los Angeles     |  22 |  16 |     - | 124\n' +
        'Arizona         |  24 |  18 |     - | 122\n' +
        'Cincinnati      |  22 |  17 |   0.5 |    \n' +
        'Chicago         |  23 |  18 |   0.5 |    \n' +
        'Miami           |  21 |  17 |   1.0 |    \n' +
        'Milwaukee       |  20 |  20 |   3.0 |    \n' +
        'New York        |  18 |  19 |   3.5 |    \n' +
        'San Diego       |  20 |  23 |   4.5 |    \n' +
        'Pittsburgh      |  16 |  19 |   4.5 |    \n' +
        'Philadelphia    |  17 |  22 |   5.5 |    \n' +
        'San Francisco   |  16 |  26 |   8.0 |    \n' +
        'Washington      |  14 |  26 |   9.0 |    \n' +
        'St. Louis       |  13 |  25 |   9.0 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Baltimore       |   5 |   1 |     - | 156\n' +
        'Boston          |   4 |   2 |   1.0 |    \n' +
        'Tampa Bay       |   3 |   3 |   2.0 |    \n' +
        'Toronto         |   2 |   4 |   3.0 |    \n' +
        'New York        |   1 |   5 |   4.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cleveland       |   5 |   1 |     - | 156\n' +
        'Kansas City     |   4 |   2 |   1.0 |    \n' +
        'Minnesota       |   3 |   3 |   2.0 |    \n' +
        'Detroit         |   2 |   4 |   3.0 |    \n' +
        'Chicago         |   1 |   5 |   4.0 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Oakland         |   5 |   1 |     - | 156\n' +
        'Los Angeles     |   4 |   2 |   1.0 |    \n' +
        'Houston         |   3 |   3 |   2.0 |    \n' +
        'Seattle         |   2 |   4 |   3.0 |    \n' +
        'Texas           |   1 |   5 |   4.0 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Boston          |   4 |   2 |     - | 157\n' +
        'Kansas City     |   4 |   2 |     - | 157\n' +
        'Los Angeles     |   4 |   2 |     - | 157\n' +
        'Houston         |   3 |   3 |   1.0 |    \n' +
        'Minnesota       |   3 |   3 |   1.0 |    \n' +
        'Tampa Bay       |   3 |   3 |   1.0 |    \n' +
        'Detroit         |   2 |   4 |   2.0 |    \n' +
        'Seattle         |   2 |   4 |   2.0 |    \n' +
        'Toronto         |   2 |   4 |   2.0 |    \n' +
        'Chicago         |   1 |   5 |   3.0 |    \n' +
        'New York        |   1 |   5 |   3.0 |    \n' +
        'Texas           |   1 |   5 |   3.0 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Philadelphia    |   5 |   1 |     - | 156\n' +
        'Washington      |   4 |   2 |   1.0 |    \n' +
        'Atlanta         |   3 |   3 |   2.0 |    \n' +
        'Miami           |   2 |   4 |   3.0 |    \n' +
        'New York        |   1 |   5 |   4.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'St. Louis       |   5 |   1 |     - | 156\n' +
        'Cincinnati      |   4 |   2 |   1.0 |    \n' +
        'Milwaukee       |   3 |   3 |   2.0 |    \n' +
        'Chicago         |   2 |   4 |   3.0 |    \n' +
        'Pittsburgh      |   1 |   5 |   4.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Los Angeles     |   5 |   1 |     - | 156\n' +
        'San Diego       |   4 |   2 |   1.0 |    \n' +
        'Colorado        |   3 |   3 |   2.0 |    \n' +
        'San Francisco   |   2 |   4 |   3.0 |    \n' +
        'Arizona         |   1 |   5 |   4.0 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |   4 |   2 |     - | 157\n' +
        'San Diego       |   4 |   2 |     - | 157\n' +
        'Washington      |   4 |   2 |     - | 157\n' +
        'Atlanta         |   3 |   3 |   1.0 |    \n' +
        'Colorado        |   3 |   3 |   1.0 |    \n' +
        'Milwaukee       |   3 |   3 |   1.0 |    \n' +
        'Chicago         |   2 |   4 |   2.0 |    \n' +
        'Miami           |   2 |   4 |   2.0 |    \n' +
        'San Francisco   |   2 |   4 |   2.0 |    \n' +
        'Arizona         |   1 |   5 |   3.0 |    \n' +
        'New York        |   1 |   5 |   3.0 |    \n' +
        'Pittsburgh      |   1 |   5 |   3.0 |    ',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Baltimore       |   0 |   0 |     - | 163\n' +
        'Boston          |   0 |   0 |     - | 163\n' +
        'New York        |   0 |   0 |     - | 163\n' +
        'Tampa Bay       |   0 |   0 |     - | 163\n' +
        'Toronto         |   0 |   0 |     - | 163\n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Chicago         |   0 |   0 |     - | 163\n' +
        'Cleveland       |   0 |   0 |     - | 163\n' +
        'Detroit         |   0 |   0 |     - | 163\n' +
        'Kansas City     |   0 |   0 |     - | 163\n' +
        'Minnesota       |   0 |   0 |     - | 163\n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Houston         |   0 |   0 |     - | 163\n' +
        'Los Angeles     |   0 |   0 |     - | 163\n' +
        'Oakland         |   0 |   0 |     - | 163\n' +
        'Seattle         |   0 |   0 |     - | 163\n' +
        'Texas           |   0 |   0 |     - | 163\n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Baltimore       |   0 |   0 |     - | 163\n' +
        'Boston          |   0 |   0 |     - | 163\n' +
        'Chicago         |   0 |   0 |     - | 163\n' +
        'Cleveland       |   0 |   0 |     - | 163\n' +
        'Detroit         |   0 |   0 |     - | 163\n' +
        'Houston         |   0 |   0 |     - | 163\n' +
        'Kansas City     |   0 |   0 |     - | 163\n' +
        'Los Angeles     |   0 |   0 |     - | 163\n' +
        'Minnesota       |   0 |   0 |     - | 163\n' +
        'New York        |   0 |   0 |     - | 163\n' +
        'Oakland         |   0 |   0 |     - | 163\n' +
        'Seattle         |   0 |   0 |     - | 163\n' +
        'Tampa Bay       |   0 |   0 |     - | 163\n' +
        'Texas           |   0 |   0 |     - | 163\n' +
        'Toronto         |   0 |   0 |     - | 163\n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Atlanta         |   0 |   0 |     - | 163\n' +
        'Miami           |   0 |   0 |     - | 163\n' +
        'New York        |   0 |   0 |     - | 163\n' +
        'Philadelphia    |   0 |   0 |     - | 163\n' +
        'Washington      |   0 |   0 |     - | 163\n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Chicago         |   0 |   0 |     - | 163\n' +
        'Cincinnati      |   0 |   0 |     - | 163\n' +
        'Milwaukee       |   0 |   0 |     - | 163\n' +
        'Pittsburgh      |   0 |   0 |     - | 163\n' +
        'St. Louis       |   0 |   0 |     - | 163\n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Arizona         |   0 |   0 |     - | 163\n' +
        'Colorado        |   0 |   0 |     - | 163\n' +
        'Los Angeles     |   0 |   0 |     - | 163\n' +
        'San Diego       |   0 |   0 |     - | 163\n' +
        'San Francisco   |   0 |   0 |     - | 163\n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Arizona         |   0 |   0 |     - | 163\n' +
        'Atlanta         |   0 |   0 |     - | 163\n' +
        'Chicago         |   0 |   0 |     - | 163\n' +
        'Cincinnati      |   0 |   0 |     - | 163\n' +
        'Colorado        |   0 |   0 |     - | 163\n' +
        'Miami           |   0 |   0 |     - | 163\n' +
        'Los Angeles     |   0 |   0 |     - | 163\n' +
        'Milwaukee       |   0 |   0 |     - | 163\n' +
        'New York        |   0 |   0 |     - | 163\n' +
        'Philadelphia    |   0 |   0 |     - | 163\n' +
        'Pittsburgh      |   0 |   0 |     - | 163\n' +
        'San Diego       |   0 |   0 |     - | 163\n' +
        'San Francisco   |   0 |   0 |     - | 163\n' +
        'St. Louis       |   0 |   0 |     - | 163\n' +
        'Washington      |   0 |   0 |     - | 163',
        'AL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Toronto         |  43 |  34 |     - |  84\n' +
        'Boston          |  40 |  36 |   2.5 |    \n' +
        'Baltimore       |  41 |  37 |   2.5 |    \n' +
        'Tampa Bay       |  39 |  38 |   4.0 |    \n' +
        'New York        |  36 |  41 |   7.0 |    \n\n' +
        'AL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Minnesota       |  44 |  32 |     - |  82\n' +
        'Kansas City     |  41 |  37 |   4.0 |    \n' +
        'Chicago         |  37 |  39 |   7.0 |    \n' +
        'Detroit         |  36 |  40 |   8.0 |    \n' +
        'Cleveland       |  35 |  40 |   8.5 |    \n\n' +
        'AL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Seattle         |  46 |  28 |     - |  77\n' +
        'Los Angeles     |  35 |  40 |  11.5 |    \n' +
        'Houston         |  33 |  42 |  13.5 |    \n' +
        'Oakland         |  32 |  43 |  14.5 |    \n' +
        'Texas           |  26 |  51 |  21.5 |    \n\n' +
        'AL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Boston          |  40 |  36 |     - |  86\n' +
        'Baltimore       |  41 |  37 |     - |  85\n' +
        'Kansas City     |  41 |  37 |     - |  85\n' +
        'Tampa Bay       |  39 |  38 |   1.5 |    \n' +
        'Chicago         |  37 |  39 |   3.0 |    \n' +
        'Detroit         |  36 |  40 |   4.0 |    \n' +
        'New York        |  36 |  41 |   4.5 |    \n' +
        'Cleveland       |  35 |  40 |   4.5 |    \n' +
        'Los Angeles     |  35 |  40 |   4.5 |    \n' +
        'Houston         |  33 |  42 |   6.5 |    \n' +
        'Oakland         |  32 |  43 |   7.5 |    \n' +
        'Texas           |  26 |  51 |  14.5 |    \n' +
        'NL East         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'New York        |  43 |  33 |     - |  85\n' +
        'Atlanta         |  41 |  35 |   2.0 |    \n' +
        'Philadelphia    |  41 |  35 |   2.0 |    \n' +
        'Washington      |  33 |  44 |  10.5 |    \n' +
        'Miami           |  25 |  51 |  18.0 |    \n\n' +
        'NL Central      |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Cincinnati      |  52 |  23 |     - |  79\n' +
        'St. Louis       |  43 |  32 |   9.0 |    \n' +
        'Chicago         |  39 |  38 |  14.0 |    \n' +
        'Milwaukee       |  37 |  40 |  16.0 |    \n' +
        'Pittsburgh      |  24 |  53 |  29.0 |    \n\n' +
        'NL West         |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'Colorado        |  46 |  29 |     - |  86\n' +
        'San Diego       |  46 |  31 |   1.0 |    \n' +
        'Los Angeles     |  43 |  31 |   2.5 |    \n' +
        'San Francisco   |  33 |  43 |  13.5 |    \n' +
        'Arizona         |  31 |  45 |  15.5 |    \n\n' +
        'NL Wild Card    |   W |   L |    GB |  M#\n' +
        '----------------|-----|-----|-------|-----\n' +
        'San Diego       |  46 |  31 |  +1.5 |  85\n' +
        'Los Angeles     |  43 |  31 |     - |  88\n' +
        'St. Louis       |  43 |  32 |   0.5 |    \n' +
        'Atlanta         |  41 |  35 |   3.0 |    \n' +
        'Philadelphia    |  41 |  35 |   3.0 |    \n' +
        'Chicago         |  39 |  38 |   5.5 |    \n' +
        'Milwaukee       |  37 |  40 |   7.5 |    \n' +
        'San Francisco   |  33 |  43 |  11.0 |    \n' +
        'Washington      |  33 |  44 |  11.5 |    \n' +
        'Arizona         |  31 |  45 |  13.0 |    \n' +
        'Miami           |  25 |  51 |  19.0 |    \n' +
        'Pittsburgh      |  24 |  53 |  20.5 |    ']


def assert_standings(standings_in, format):
  appTest = AppTest(standings_in=standings_in)
  appTest.setup()
  assert_equals(appTest.process_standings(), format)


def test():
  for i, o in zip(inpt, outp):
    assert_standings(i, o)

if __name__ == '__main__':
  test()
