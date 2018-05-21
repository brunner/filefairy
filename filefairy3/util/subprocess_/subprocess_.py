#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import threading


class Command(object):
    def __init__(self, cmd):
        self.output = {'ok': True}
        self.proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run(self, timeout):
        try:
            t = threading.Thread(target=self._target)
            t.start()

            if timeout:
                t.join(timeout)
                if t.is_alive():
                    self.proc.terminate()
                    self.output.update({'ok': False, 'error': 'timeout'})

            t.join()
        except Exception as e:
            self.output.update({
                'ok': False,
                'error': 'exception',
                'exception': str(e)
            })

        return self.output

    def _target(self):
        stdout, _ = self.proc.communicate()
        if stdout:
            self.output.update({'output': stdout.decode('utf-8')})


def check_output(cmd, timeout=0):
    return Command(cmd).run(timeout)
