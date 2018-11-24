#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extend the reloadable API to enable dynamic loading of services in a task.

This base class creates a mechanism for importing and calling methods belonging
to arbitrary service modules. This preserves a task's ability to be reloaded
by the main app by giving the task the means to refresh its own dependencies
at the same time.

Example:
    class Task(Reloadable):
        def __init__(self, **kwargs):
            super(Task, self).__init__(**kwargs)

        def _reload_internal(self, **kwargs):
            return {'a': ['foo', 'bar'], 'b': ['baz']}

If the _reload method is invoked, the task will import both ``a`` and ``b``,
and retrieve and store service methods ``foo``, ``bar``, and ``baz``. The
method _call can then be invoked with the name of the service method and any
arguments, and it will dispatch the call to the corresponding service.
"""

import abc
import importlib
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/api/reloadable', '', _path))


class Reloadable():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attrs = {}

    def _call(self, method, fargs, *args, **kwargs):
        self.attrs[method](*fargs, *args, **kwargs)

    @abc.abstractmethod
    def _reload_internal(self, **kwargs):
        pass

    def _reload(self, **kwargs):
        services = self._reload_internal(**kwargs)
        for service in services:
            package = 'services.{}.{}'.format(service, service)
            module = importlib.import_module(package)

            for method in services[service]:
                self.attrs[method] = getattr(module, method)
