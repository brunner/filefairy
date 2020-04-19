#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for messageable classes."""


def messageable(f):
    """Decorator indicating that a function is messageable."""
    f._messageable = True
    return f
