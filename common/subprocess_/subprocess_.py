#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for subprocess commands."""

import logging
import subprocess

_logger = logging.getLogger('filefairy')


def check_output(cmd, log=True, timeout=None):
    """Convenience wrapper around subprocess.run.

    Args:
        cmd: List of arguments used to launch the process.
        log: Whether or not to log any caught exceptions.
        timeout: Whether to timeout the process after a number of seconds.

    Returns:
        A representation of whether the command finished successfully, as well
        as stdout and stderr captured from the return value of subprocess.run.
    """
    output = {'ok': True, 'stdout': '', 'stderr': ''}
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=True)
        if isinstance(proc, subprocess.CompletedProcess):
            output.update({'stdout': proc.stdout.decode('utf-8')})
            output.update({'stderr': proc.stderr.decode('utf-8')})
    except subprocess.SubprocessError as e:
        if log:
            _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)
        output.update({'ok': False, 'stdout': str(e), 'stderr': str(e)})

    return output
