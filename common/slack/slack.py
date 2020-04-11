#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for Slack API integrations."""

import logging
import json
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/slack', '', _path))

from common.secrets.secrets import filefairy  # noqa
from common.urllib_.urllib_ import urlopen  # noqa

FILEFAIRY = filefairy()


def _call(method, params):
    """Helper function for calling Slack API endpoints.

    Args:
        method: The endpoint name.
        params: Params to pass to the endpoint.

    Returns:
        The endpoint response.
    """
    url = 'https://slack.com/api/{}'.format(method)
    obj = {'ok': False}

    # TODO: uncomment after finishing refactors.
    # try:
    #     response = urlopen(url, params).decode('utf-8')
    #     obj = json.loads(response)
    # except Exception:
    #     _logger.log(logging.WARNING, 'Handled warning.', exc_info=True)

    return obj


def channels_history(channel, latest, oldest):
    """Convenience wrapper around the Slack API channels.history endpoint.

    Args:
        channel: Channel to fetch history for.
        latest: End of time range of messages to include in results.
        oldest: Beginning of time range of messages to include in results.

    Returns:
        The endpoint response.
    """
    return _call('channels.history', {
        'token': FILEFAIRY,
        'channel': channel,
        'count': 1000,
        'latest': latest,
        'oldest': oldest,
    })


def channels_list():
    """Convenience wrapper around the Slack API channels.list endpoint.

    Returns:
        The endpoint response.
    """
    return _call('channels.list', {
        'token': FILEFAIRY,
        'exclude_members': True,
        'exclude_archived': True
    })


def chat_post_message(channel, text, attachments=[]):
    """Convenience wrapper around the Slack API chat.postMessage endpoint.

    Args:
        channel: Channel to send message to.
        text: Text of the message to send.
        attachments: A JSON-based array of structured attachments.

    Returns:
        The endpoint response.
    """
    return _call(
        'chat.postMessage', {
            'token': FILEFAIRY,
            'channel': channel,
            'text': text,
            'as_user': 'true',
            'attachments': attachments,
            'link_names': 'true'
        })


def files_upload(content, filename, channel):
    """Convenience wrapper around the Slack API files.upload endpoint.

    Args:
        content: File contents.
        filename: Filename of file.
        channel: Channel where the file will be shared.

    Returns:
        The endpoint response.
    """
    return _call(
        'files.upload', {
            'token': FILEFAIRY,
            'content': content,
            'filename': filename,
            'channels': channel,
        })


def pins_add(channel, timestamp):
    """Convenience wrapper around the Slack API pins.add endpoint.

    Args:
        channel: Channel to pin the item in.
        filename: Timestamp of the message to pin.

    Returns:
        The endpoint response.
    """
    return _call('pins.add', {
        'token': FILEFAIRY,
        'channel': channel,
        'timestamp': timestamp,
    })


def reactions_add(name, channel, timestamp):
    """Convenience wrapper around the Slack API reactions.add endpoint.

    Args:
        name: Reaction (emoji) name.
        channel: Channel where the message to add reaction to was posted.
        filename: Timestamp of the message to add reaction to.

    Returns:
        The endpoint response.
    """
    return _call(
        'reactions.add', {
            'token': FILEFAIRY,
            'name': name,
            'channel': channel,
            'timestamp': timestamp,
        })


def reactions_get(channel, timestamp):
    """Convenience wrapper around the Slack API reactions.get endpoint.

    Args:
        channel: Channel where the message to get reactions for was posted.
        filename: Timestamp of the message to get reactions for.

    Returns:
        The endpoint response.
    """
    return _call('reactions.get', {
        'token': FILEFAIRY,
        'channel': channel,
        'timestamp': timestamp,
    })


def reactions_remove(name, channel, timestamp):
    """Convenience wrapper around the Slack API reactions.remove endpoint.

    Args:
        name: Reaction (emoji) name.
        channel: Channel where the message to remove reaction from was posted.
        filename: Timestamp of the message to remove reaction from.

    Returns:
        The endpoint response.
    """
    return _call(
        'reactions.remove', {
            'token': FILEFAIRY,
            'name': name,
            'channel': channel,
            'timestamp': timestamp,
        })


def rtm_connect():
    """Convenience wrapper around the Slack API rtm.connect endpoint.

    Returns:
        The endpoint response.
    """
    return _call('rtm.connect', {'token': FILEFAIRY})


def users_list():
    """Convenience wrapper around the Slack API users.list endpoint.

    Returns:
        The endpoint response.
    """
    return _call('users.list', {'token': FILEFAIRY})
