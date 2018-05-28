#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc


class Runnable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def _run_internal(self, **kwargs):
        pass

    def _run(self, **kwargs):
        return self._run_internal(**kwargs)
