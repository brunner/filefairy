#!/usr/bin/env python

from league_file_plugin import LeagueFilePlugin, get_data

import mock
import os
import re
import unittest
import sys

sys.path.append(re.sub(r'/plugins/league_file', '', os.path.dirname(__file__)))
from utils.testing.testing_util import overwrite


started = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 310000000 Jan 29 19:26 orange_and_blue_league_baseball.tar.gz.filepart
"""

stopped = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 19:30 orange_and_blue_league_baseball.tar.gz
"""

with_null_data = '{"filepart": null, "finished": []}'

with_null_data_after_started = '{"finished": [], "filepart": {' + \
    '"start": "Jan 29 19:26", "end": "Jan 29 19:26", "size": "310000000"}}'

with_filepart = '{"filepart": {"size": "300000000", "start": "Jan 29 15:00", ' + \
    '"end": "Jan 29 19:23"}, "finished": []}'

with_filepart_after_started = '{"finished": [], "filepart": {' + \
    '"start": "Jan 29 15:00", "end": "Jan 29 19:26", "size": "310000000"}}'

with_filepart_after_stopped = '{"finished": [{"start": "Jan 29 15:00", ' + \
    '"end": "Jan 29 19:30", "size": "328706052"}], "filepart": null}'

with_finished = '{"filepart": null, "finished": [{"size": "345678901", ' + \
    '"start": "Jan 27 08:00", "end": "Jan 27 12:00"}]}'

with_finished_after_started = '{"finished": [{"start": "Jan 27 08:00", ' + \
    '"end": "Jan 27 12:00", "size": "345678901"}], "filepart": {' + \
    '"start": "Jan 29 19:26", "end": "Jan 29 19:26", "size": "310000000"}}'

with_finished_after_stopped = '{"filepart": null, "finished": [{' + \
    '"size": "345678901", "start": "Jan 27 08:00", "end": "Jan 27 12:00"}]}'

with_filepart_and_finished = '{"filepart": {"size": "300000000", ' + \
    '"start": "Jan 29 15:00", "end": "Jan 29 19:23"}, "finished": [{' + \
    '"size": "345678901", "start": "Jan 27 08:00", "end": "Jan 27 12:00"}]}'

with_filepart_and_finished_after_started = '{"finished": [{' + \
    '"start": "Jan 27 08:00", "end": "Jan 27 12:00", "size": "345678901"}], ' + \
    '"filepart": {"start": "Jan 29 15:00", "end": "Jan 29 19:26", "size": "310000000"}}'

with_filepart_and_finished_after_stopped = '{"finished": [{' + \
    '"start": "Jan 29 15:00", "end": "Jan 29 19:30", "size": "328706052"}, ' + \
    '{"start": "Jan 27 08:00", "end": "Jan 27 12:00", "size": "345678901"}], "filepart": null}'


class LeagueFilePluginTest(unittest.TestCase):

  @mock.patch('subprocess.check_output', return_value=started)
  def test_run__started__with_null_data(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_null_data)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertEqual(plugin.filepart['size'], '310000000')
    self.assertEqual(plugin.filepart['start'], 'Jan 29 19:26')
    self.assertEqual(plugin.filepart['end'], 'Jan 29 19:26')
    self.assertEqual(len(plugin.finished), 0)

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_null_data_after_started)

  @mock.patch('subprocess.check_output', return_value=started)
  def test_run__started__with_filepart(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_filepart)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertEqual(plugin.filepart['size'], '310000000')
    self.assertEqual(plugin.filepart['start'], 'Jan 29 15:00')
    self.assertEqual(plugin.filepart['end'], 'Jan 29 19:26')
    self.assertEqual(len(plugin.finished), 0)

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_filepart_after_started)

  @mock.patch('subprocess.check_output', return_value=started)
  def test_run__started__with_finished(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_finished)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertEqual(plugin.filepart['size'], '310000000')
    self.assertEqual(plugin.filepart['start'], 'Jan 29 19:26')
    self.assertEqual(plugin.filepart['end'], 'Jan 29 19:26')
    self.assertEqual(len(plugin.finished), 1)
    self.assertEqual(plugin.finished[0]['size'], '345678901')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 27 08:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 27 12:00')

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_finished_after_started)

  @mock.patch('subprocess.check_output', return_value=started)
  def test_run__started__with_filepart_and_finished(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_filepart_and_finished)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertEqual(plugin.filepart['size'], '310000000')
    self.assertEqual(plugin.filepart['start'], 'Jan 29 15:00')
    self.assertEqual(plugin.filepart['end'], 'Jan 29 19:26')
    self.assertEqual(len(plugin.finished), 1)
    self.assertEqual(plugin.finished[0]['size'], '345678901')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 27 08:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 27 12:00')

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_filepart_and_finished_after_started)

  @mock.patch('subprocess.check_output', return_value=stopped)
  def test_run__stopped__with_null_data(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_null_data)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertIsNone(plugin.filepart)
    self.assertEqual(len(plugin.finished), 0)

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_null_data)

  @mock.patch('subprocess.check_output', return_value=stopped)
  def test_run__stopped__with_filepart(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_filepart)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertIsNone(plugin.filepart)
    self.assertEqual(len(plugin.finished), 1)
    self.assertEqual(plugin.finished[0]['size'], '328706052')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 29 15:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 29 19:30')

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_filepart_after_stopped)

  @mock.patch('subprocess.check_output', return_value=stopped)
  def test_run__stopped__with_finished(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_finished)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertIsNone(plugin.filepart)
    self.assertEqual(len(plugin.finished), 1)
    self.assertEqual(plugin.finished[0]['size'], '345678901')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 27 08:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 27 12:00')

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_finished_after_stopped)

  @mock.patch('subprocess.check_output', return_value=stopped)
  def test_run__stopped__with_filepart_and_finished(self, subprocess_check_output_mock):
    original = overwrite(get_data(), with_filepart_and_finished)

    plugin = LeagueFilePlugin()
    plugin.run()

    self.assertIsNone(plugin.filepart)
    self.assertEqual(len(plugin.finished), 2)
    self.assertEqual(plugin.finished[0]['size'], '328706052')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 29 15:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 29 19:30')
    self.assertEqual(plugin.finished[1]['size'], '345678901')
    self.assertEqual(plugin.finished[1]['start'], 'Jan 27 08:00')
    self.assertEqual(plugin.finished[1]['end'], 'Jan 27 12:00')

    changed = overwrite(get_data(), original)
    self.assertEqual(changed, with_filepart_and_finished_after_stopped)


if __name__ == '__main__':
    unittest.main()
