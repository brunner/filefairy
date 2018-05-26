#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess


def check_output(cmd, timeout=None):
    output = {'ok': True}
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=True)
        if isinstance(proc, subprocess.CompletedProcess):
            output.update({'output': proc.stdout.decode('utf-8')})
    except subprocess.SubprocessError as e:
        output.update({'ok': False, 'output': str(e)})

    return output
