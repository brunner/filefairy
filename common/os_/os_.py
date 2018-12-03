#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for OS operations."""

import contextlib
import logging
import os
import re

_logger = logging.getLogger('fairylab')

FILEFAIRY_DIR = re.sub(r'/common/os_', '',
                       os.path.dirname(os.path.abspath(__file__)))


@contextlib.contextmanager
def chdir(path):
    """Convenience wrapper around os.chdir.

    Defines a context manager which changes the working directory to the given
    path, and restores the original path upon exiting.

    Args:
        path: The directory to change to.
    """
    try:
        cwd = os.getcwd()
    except Exception:
        _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
        cwd = FILEFAIRY_DIR

    os.chdir(path)

    try:
        yield
    except Exception:
        _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
    finally:
        os.chdir(cwd)
