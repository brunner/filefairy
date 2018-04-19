#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import datetime
import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/download', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.datetime.datetime_util import decode_datetime, encode_datetime  # noqa
from utils.file.file_util import wget_file  # noqa
from utils.unicode.unicode_util import deunicode  # noqa


class DownloadPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(DownloadPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Manages file download and data extraction.'

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if activity == ActivityEnum.FILE:
            t = threading.Thread(target=self._download)
            t.daemon = True
            t.start()
            return True
        return False

    def _on_message_internal(self, **kwargs):
        return ActivityEnum.NONE

    def _run_internal(self, **kwargs):
        if self.data['downloaded']:
            self.data['downloaded'] = False
            self.write()
            return ActivityEnum.DOWNLOAD

        return ActivityEnum.NONE

    def _setup_internal(self, **kwargs):
        pass

    def _download(self):
        wget_file()
        self.data['then'] = self.data['now']

        self._games()
        self._leagues()

        self.data['downloaded'] = True
        self.write()

    def _games(self):
        boxes = 'download/news/html/box_scores'
        leagues = 'download/news/txt/leagues'
        for box in os.listdir(os.path.join(_root, boxes)):
            bdname = os.path.join(_root, 'extract/box_scores', box)
            bfname = os.path.join(_root, boxes, box)
            log = box.replace('game_box', 'log').replace('html', 'txt')
            ldname = os.path.join(_root, 'extract/game_logs', log)
            lfname = os.path.join(_root, leagues, log)
            if not os.path.isfile(bfname) or not os.path.isfile(lfname):
                continue
            self._games_internal(bdname, bfname, ldname, lfname)

    def _games_internal(self, bdname, bfname, ldname, lfname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with open(bfname, 'r') as bff:
            bcontent = bff.read()
        with open(lfname, 'r') as lff:
            lcontent = lff.read()

        pattern = 'MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})'
        match = re.findall(pattern, bcontent)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            if date >= then:
                with open(bdname, 'w') as bdf:
                    bdf.write(bcontent)
                with open(ldname, 'w') as ldf:
                    ldf.write(lcontent)
            if date >= now:
                now = date + datetime.timedelta(days=1)

        self.data['now'] = encode_datetime(now)

    def _leagues(self):
        leagues = 'download/news/txt/leagues'
        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        fpath = os.path.join(_root, leagues, 'league_100_{}.txt')
        for key in ['injuries', 'news', 'transactions']:
            dname = dpath.format(key)
            fname = fpath.format(key)
            if not os.path.isfile(dname) or not os.path.isfile(fname):
                continue
            self._leagues_internal(key, dname, fname)

    def _leagues_internal(self, key, dname, fname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with codecs.open(fname, 'r', encoding='utf-8', errors='replace') as ff:
            content = deunicode(ff.read())

        with open(dname, 'w') as df:
            match = re.findall('\d{8}\t[^\n]+\n', content.strip() + '\n')
            for m in match:
                date = datetime.datetime.strptime(m[:8], '%Y%m%d')
                if date >= then:
                    df.write(m)
                if date > now:
                    now = date

        self.data['now'] = encode_datetime(now)
