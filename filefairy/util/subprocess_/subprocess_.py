#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import subprocess

logger_ = logging.getLogger('fairylab')


def check_output(cmd, log=True, timeout=None):
    output = {'ok': True}
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
            logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
        output.update({'ok': False, 'stdout': str(e), 'stderr': str(e)})

    return output
