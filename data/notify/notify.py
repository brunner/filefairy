#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for status notifications."""

from enum import IntEnum


class Notify(IntEnum):
    """Describe a number of different app and task status changes."""

    # An arbitrary task has performed some arbitrary behavior. The app should
    # note the task activity but does not need to relay the notification to
    # other tasks.
    BASE = 1

    # The download task has determined that the file has been downloaded and
    # extracted, and is ready for consumption by the other tasks.
    DOWNLOAD_FINISH = 2

    # The download task has determined from the extracted file data that
    # January 1st has passed in the simulation.
    DOWNLOAD_YEAR = 3

    # The exports task has determined that the emailed exports were loaded.
    EXPORTS_EMAILS = 4

    # The app has determined that midnight PST has passed, in real life.
    FILEFAIRY_DAY = 5

    # The app has determined that some rendering has changed, and relays the
    # information to the git task to deploy the rendering changes to Fairylab.
    FILEFAIRY_DEPLOY = 6

    # The statsplus task has determined that all scores from the latest
    # league file have been parsed.
    STATSPLUS_FINISH = 7

    # The statsplus task has determined that some scores from the latest
    # statsplus messages have been parsed.
    STATSPLUS_PARSE = 8

    # The statsplus task has determined that a simulation has started.
    STATSPLUS_START = 9

    # The upload task has determined that the file upload has finished.
    UPLOAD_FINISH = 10

    # An arbitrary value for use in tests.
    OTHER = 11
