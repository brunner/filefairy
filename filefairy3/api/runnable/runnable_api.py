#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class RunnableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(RunnableApi, self).__init__()

    @abc.abstractmethod
    def _run_internal(self, **kwargs):
        pass

    def _run(self, **kwargs):
        return self._run_internal(**kwargs)
