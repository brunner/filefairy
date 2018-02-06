#!/usr/bin/env python

import abc


class NameableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(NameableApi, self).__init__()

    @abc.abstractmethod
    def _name(self):
        pass
