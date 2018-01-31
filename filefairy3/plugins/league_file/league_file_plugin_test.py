#!/usr/bin/env python

from league_file_plugin import LeagueFilePlugin

import mock
import unittest


stopped = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 19:24 orange_and_blue_league_baseball.tar.gz
"""


class LeagueFilePluginTest(unittest.TestCase):

  @mock.patch('subprocess.check_output', return_value=stopped)
  def test_run__stopped__with_filepart(self, subprocess_check_output_mock):
    plugin = LeagueFilePlugin()
    plugin.filepart = {'size': '300000000', 'start': 'Jan 29 15:00', 'end': 'Jan 29 19:23'}
    plugin.run()

    self.assertIsNone(plugin.filepart)
    self.assertEqual(plugin.finished[0]['size'], '328706052')
    self.assertEqual(plugin.finished[0]['start'], 'Jan 29 15:00')
    self.assertEqual(plugin.finished[0]['end'], 'Jan 29 19:24')


if __name__ == '__main__':
    unittest.main()
