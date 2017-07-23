#!/usr/bin/env python

import argparse
import os
import sys

# Replace these values with your own information.
leaguefile = "orangeandblue.lg"


def getLeaguePath():
  if sys.platform == "cygwin":
    # Replace this with your Windows username, if applicable.
    username = "Username"
    return os.path.join("C:", "Users", username, "My Documents",
                        "Out of the Park Developments", "OOTP Baseball 17",
                        "saved_games", leaguefile)
  else:
    return os.path.join(os.path.expanduser("~"),
                        ".Out of the Park Developments", "OOTP Baseball 17",
                        "custdata", "saved_games", leaguefile)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--recover', dest='recover', action='store_true')
  parser.set_defaults(recover=False)
  args = parser.parse_args()

  host = "http://www.orangeandblueleaguebaseball.com/league_file/"
  importfile = "orange_and_blue_league_baseball.tar.gz"
  leaguepath = getLeaguePath()
  backuppath = "{0}.bk".format(leaguepath)

  if args.recover:
    if os.path.isdir(backuppath):
      os.system("rm -rf '{0}' && mv '{1}' '{0}'".format(leaguepath, backuppath))
  else:
    if os.path.isdir(leaguepath):
      os.system("rm -rf '{0}' && mv '{1}' '{0}'".format(backuppath, leaguepath))

    os.system("rm -rf '{0}' && mkdir '{0}'".format(leaguepath))
    os.chdir(leaguepath)

    os.system("wget {0}{1}".format(host, importfile))
    os.system("tar -xzf {0}".format(importfile))
    os.system("rm {0}".format(importfile))

    dirs = ["ballcaps", "jerseys", "news/html/images",
            "news/html/images/profile_pictures", "settings"]
    for d in dirs:
      os.system("rm -rf '{0}' && cp -R '{1}' '{0}'".format(os.path.join(
          leaguepath, d), os.path.join(backuppath, d)))

if __name__ == "__main__":
  main()
