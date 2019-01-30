#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for calling reloadable services."""

import importlib
import re
import os
import sys
import types

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/service', '', _path))
_services = {}

from common.os_.os_ import listdirs  # noqa

SERVICES_DIR = re.sub(r'/common/service', '/services', _path)


def _reload(service):
    package = 'services.{}.{}'.format(service, service)

    if package in sys.modules:
        sys.modules.pop(package, None)

    _services[service] = importlib.import_module(package)


def call_service(service, method, fargs, *args, **kwargs):
    """Calls the specified service method.

    Args:
        service: The service name.
        method: The method name.
        fargs: The formal arguments to pass to the method.
        args: The variable arguments to pass to the method.
        kwargs: The keyword arguments to pass to the method.
    """
    return getattr(_services[service], method)(*fargs, *args, **kwargs)


def mock_service_for_test(service, method, mock):
    m = types.ModuleType(service, None)
    m.__file__ = service + '.py'
    _services[service] = m
    setattr(m, method, mock)


def reload_service_for_test(service):
    """Reloads the specified service only."""
    _reload(service)


def reload_services():
    """Reloads the services."""
    for s in listdirs(SERVICES_DIR):
        _reload(s)
