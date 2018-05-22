#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/download', '', _path)
sys.path.append(_root)
from api.plugin.plugin import Plugin  # noqa
from api.serializable.serializable import Serializable  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.file_.file_ import ping  # noqa
from util.file_.file_ import recreate  # noqa
from util.file_.file_ import wget_file  # noqa
from util.logger.logger import log  # noqa
from value.notify.notify import Notify  # noqa
from value.response.response import Response  # noqa


class Download(Plugin, Serializable):
    def __init__(self, **kwargs):
        super(Download, self).__init__(**kwargs)

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
        notify = kwargs['notify']
        response = Response()
        if notify == Notify.LEAGUEFILE_FINISH:
            self.download(**kwargs)
            response.notify = [Notify.BASE]
        return response

    def _on_message_internal(self, **kwargs):
        return Response()

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = Response()

        if self.data['year']:
            self.data['year'] = False
            response.append_notify(Notify.DOWNLOAD_YEAR)

        if self.data['downloaded']:
            self.data['downloaded'] = False
            response.append_notify(Notify.DOWNLOAD_FINISH)
            response.shadow = self._shadow_internal(**kwargs)

        if data != original:
            self.write()

        return response

    def _setup_internal(self, **kwargs):
        return Response()

    def _shadow_internal(self, **kwargs):
        return {'statsplus': {'download.now': self.data['now']}}

    def download(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        output = ping()
        if output.get('ok'):
            log(self._name(), **dict(kwargs, s='Download started.'))
            t = threading.Thread(target=self._download_internal, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            log(self._name(),
                **dict(kwargs, c=output, s='Download failed.', v=True))

        if data != original:
            self.write()

    def _download_internal(self, **kwargs):
        self.data['then'] = self.data['now']

        wget_file()
        self._games()
        self._leagues()

        self.data['downloaded'] = True
        log(self._name(), **dict(kwargs, s='Download finished.'))

        dthen = decode_datetime(self.data['then'])
        dnow = decode_datetime(self.data['now'])
        if dthen.year != dnow.year:
            self.data['year'] = True

        self.write()

    def _games(self):
        box_scores = os.path.join(_root, 'extract/box_scores')
        game_logs = os.path.join(_root, 'extract/game_logs')
        recreate(box_scores)
        recreate(game_logs)

        boxes = 'download/news/html/box_scores'
        leagues = 'download/news/txt/leagues'
        for box in os.listdir(os.path.join(_root, boxes)):
            bdname = os.path.join(box_scores, box)
            bfname = os.path.join(_root, boxes, box)
            log_ = box.replace('game_box', 'log').replace('html', 'txt')
            ldname = os.path.join(game_logs, log_)
            lfname = os.path.join(_root, leagues, log_)
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

        with open(fname, 'r', encoding='iso-8859-1') as ff:
            content = ff.read()

        with open(dname, 'w') as df:
            match = re.findall('\d{8}\t[^\n]+\n', content.strip() + '\n')
            for m in match:
                date = datetime.datetime.strptime(m[:8], '%Y%m%d')
                if date >= then:
                    df.write(m)
                if date > now:
                    now = date

        self.data['now'] = encode_datetime(now)
