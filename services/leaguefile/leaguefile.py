#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for leaguefile operations."""

import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/leaguefile', '', _path))

from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_est  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.re_.re_ import find  # noqa
from common.secrets.secrets import server  # noqa
from common.subprocess_.subprocess_ import check_output  # noqa

ARCHIVE_REGEX = r'(\d+)\s(\w+\s\d+\s\d+:\d+)\sorange_and_blue_league_baseball'
DOWNLOAD_DIR = re.sub(r'/services/leaguefile', '/resource/download', _path)
DOWNLOAD_BOX_SCORES = os.path.join(DOWNLOAD_DIR, 'news/html/box_scores')
DOWNLOAD_LEAGUES = os.path.join(DOWNLOAD_DIR, 'news/txt/leagues')
EXTRACT_DIR = re.sub(r'/services/leaguefile', '/resource/extract', _path)
EXTRACT_BOX_SCORES = os.path.join(EXTRACT_DIR, 'box_scores')
EXTRACT_GAME_LOGS = os.path.join(EXTRACT_DIR, 'game_logs')
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')
SERVER = server()


def download_file(url):
    """Download and unpack the league file.

    Args:
        url: The url of the league file.

    Returns:
        Subprocess output describing the download status.
    """
    check_output(['rm', '-rf', DOWNLOAD_DIR])
    check_output(['mkdir', DOWNLOAD_DIR])

    cwd = os.getcwd()
    os.chdir(DOWNLOAD_DIR)

    output = check_output(['wget', url], timeout=4800)
    if output.get('ok'):
        filename = url.rsplit('/', 1)[1]
        check_output(['tar', '-xzf', filename])

    os.chdir(cwd)
    return output


def extract_file(start):
    """Extract the relevant parts of the league file.

    The league file contains many months of data from many leagues, but the
    goal is to only extract data pertaining to the MLB that is newer than the
    previously extracted data. A start date is provided as input, and the
    function extracts anything newer than it before returning a computed end
    date, which can then be reused as the start date of the next extraction.

    Args:
        start: The start date for the extraction.

    Returns:
        The end date for the extraction.
    """
    for d in [EXTRACT_BOX_SCORES, EXTRACT_GAME_LOGS, EXTRACT_LEAGUES]:
        check_output(['rm', '-rf', d])
        check_output(['mkdir', d])

    end = start
    for box in os.listdir(DOWNLOAD_BOX_SCORES):
        box_fname = os.path.join(DOWNLOAD_BOX_SCORES, box)
        if not os.path.isfile(box_fname):
            continue

        game = box.replace('game_box', 'log').replace('html', 'txt')
        game_fname = os.path.join(DOWNLOAD_LEAGUES, game)
        if not os.path.isfile(game_fname):
            continue

        with open(box_fname, 'r', encoding='iso-8859-1') as f:
            box_read = f.read()

        with open(game_fname, 'r', encoding='iso-8859-1') as f:
            game_read = f.read()

        match = find('MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})', box_read)
        if not match:
            continue

        d = datetime.datetime.strptime(match, '%m/%d/%Y')
        date = datetime_datetime_pst(d.year, d.month, d.day)
        if date < start:
            continue

        with open(os.path.join(EXTRACT_BOX_SCORES, box), 'w') as f:
            f.write(box_read)

        with open(os.path.join(EXTRACT_GAME_LOGS, game), 'w') as f:
            f.write(game_read)

        if date >= end:
            end = date + datetime.timedelta(days=1)

    for key in ['injuries.txt', 'news.txt', 'transactions.txt']:
        fname = os.path.join(DOWNLOAD_LEAGUES, 'league_100_{}'.format(key))
        if not os.path.isfile(fname):
            continue

        with open(fname, 'r', encoding='iso-8859-1') as f:
            read = f.read()

        write = []
        for m in re.findall('(\d{8}\t[^\n]+)\n', read.strip() + '\n'):
            d = datetime.datetime.strptime(m[:8], '%Y%m%d')
            date = datetime_datetime_pst(d.year, d.month, d.day)

            if date < start:
                continue
            elif date > end:
                end = date

            write.append(m)

        with open(os.path.join(EXTRACT_LEAGUES, key), 'w') as f:
            f.write('\n'.join(write) + '\n')

    return end


def find_download(now):
    """Get the current information about the downloaded league file.

    The league file could either be in an ``ongoing`` (currently downloading)
    state or a ``done`` state. The information determined by this function
    includes that state, as well as the file's size and timestamp. The year of
    the timestamp is inferred from a datetime object that is passed to the
    function.

    Args:
        now: A datetime object for the current date and time.

    Returns:
        The size, timestamp, and state of the downloaded league file.
    """
    output = check_output(['ls', '-l', DOWNLOAD_DIR], timeout=8)
    if output.get('ok'):
        stdout = re.sub(r'[ ]+', ' ', output.get('stdout', ''))
        ongoing = 'news' not in stdout
        for line in stdout.splitlines():
            size, s = find(ARCHIVE_REGEX, line)
            if size:
                d = datetime.datetime.strptime(s, '%b %d %H:%M')
                date = datetime_datetime_pst(now.year, d.month, d.day, d.hour,
                                             d.minute)
                return (size, date, ongoing)


def find_upload(now):
    """Get the current information about the uploaded league file.

    The league file could either be in an ``ongoing`` (currently uploading)
    state or a ``done`` state. The information determined by this function
    includes that state, as well as the file's size and timestamp. The year of
    the timestamp is inferred from a datetime object that is passed to the
    function. Note that the timestamp scraped from the ``ls`` command output is
    displayed in Eastern time, so we need to fix the localization to match all
    of the other dates which are stored by the main app in Pacific time.

    Args:
        now: A datetime object for the current date and time.

    Returns:
        The size, timestamp, and state of the uploaded league file.
    """
    ls = 'ls -l /var/www/html/StatsLab/league_file'
    output = check_output(['ssh', 'brunnerj@' + SERVER, ls], timeout=8)
    if output.get('ok'):
        stdout = re.sub(r'[ ]+', ' ', output.get('stdout', ''))
        ongoing = '.filepart' in stdout
        for line in stdout.splitlines():
            size, s = find(ARCHIVE_REGEX, line)
            if size and ('.filepart' in line) == ongoing:
                d = datetime.datetime.strptime(s, '%b %d %H:%M')
                date = datetime_datetime_est(now.year, d.month, d.day, d.hour,
                                             d.minute)
                return (size, datetime_as_pst(date), ongoing)
