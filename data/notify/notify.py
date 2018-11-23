#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data (non-reloadable) object for status notifications."""

from enum import Enum


class Notify(Enum):
    """Describe a number of different app and task status changes."""

    # An arbitrary task has performed some arbitrary behavior. The app should
    # note the task activity but does not need to relay the notification to
    # other tasks.
    BASE = 1

    # The exports task has determined that the emailed exports were loaded.
    EXPORTS_EMAILS = 2

    # The app has determined that midnight PST has passed, in real life.
    FILEFAIRY_DAY = 3

    # The app has determined that some rendering has changed, and relays the
    # information to the git task to deploy the rendering changes to Fairylab.
    FILEFAIRY_DEPLOY = 4

    # The leaguefile task has determined that the file has been downloaded and
    # extracted, and is ready for consumption by the other tasks.
    LEAGUEFILE_DOWNLOAD = 5

    # The leaguefile task has determined that the file upload has finished.
    LEAGUEFILE_FINISH = 6

    # The leaguefile task has determined that the file upload has started.
    LEAGUEFILE_START = 7

    # The leaguefile task has determined from the extracted file data that
    # January 1st has passed, in the simulation.
    LEAGUEFILE_YEAR = 8

    # The statsplus task has determined that a simulation is ongoing.
    STATSPLUS_SIM = 9

    # An arbitrary value for use in tests.
    OTHER = 10
