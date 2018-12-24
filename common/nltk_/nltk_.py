#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common (non-reloadable) util methods for natural language processing."""

import html
import nltk
import nltk.probability as probability
import os
import random
import re
import sys

from nltk.util import ngrams

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/common/nltk_', '', _path))

from common.re_.re_ import find  # noqa
from common.slack.slack import channels_history  # noqa
from common.slack.slack import channels_list  # noqa
from common.slack.slack import users_list  # noqa

CORPUS_DIR = re.sub(r'/common/nltk_', '/resource/corpus', _path)

CHANNEL_PATTERN = r'^<\#\w+\|\w+>$'
EMOJI_PATTERN = r'^:[^:]+:$'
USER_PATTERN = r'^<@\w+>$'

SPECIAL_PATTERN = r'|'.join([EMOJI_PATTERN, CHANNEL_PATTERN, USER_PATTERN])


def _cond_samples(grams):
    for gram in grams:
        n = len(gram) - 1
        yield tuple(t.lower() for t in gram[:n]), gram[n]


def get_cfd(n, messages):
    """Generates a ConditionalFreqDist from a set of messages.

    Args:
        n: The order of N for the n-grams contained in the CFD.
        messages: The messages to add to the CFD.

    Returns:
        The generated CFD.
    """
    tokens = []
    for message in messages:
        tokens += word_tokenize(message)

    grams = []
    for i in range(2, n + 1):
        grams += ngrams(tokens, i)

    return probability.ConditionalFreqDist(_cond_samples(grams))


def get_messages():
    """Creates a dictionary containing public channel history, keyed by user.

    Returns:
        The dictionary of messages.
    """
    messages = {}

    list_ = channels_list()
    if not list_['ok']:
        return None

    for channel in list_['channels']:
        latest = ''
        while True:
            history = channels_history(channel['id'], latest)
            if not history['ok']:
                break

            for message in history['messages']:
                if not all(k in message for k in ['text', 'ts', 'user']):
                    continue

                latest = message['ts']
                text = message['text']
                user = message['user']

                if user == 'U3ULC7DBP' and channel['id'] != 'C9YE6NQG0':
                    continue

                for t in text.splitlines():
                    u = html.unescape(re.sub(r'<[^>]+>|[()]', '', t)).strip()

                    if u:
                        if not find(r'[.?!:,]$', u):
                            u += '.'

                        if user not in messages:
                            messages[user] = []
                        messages[user].append(u)

            if not history['has_more']:
                break

    return messages


def get_topic(cfd):
    """Fetches a random condition from a CFD to use as a topic.

    Args:
        cfd: The conditional frequency distribution of words to reference.

    Returns:
        The random CFD condition.
    """
    conds = list(filter(lambda c: find(r'^\w', c[0]), cfd.conditions()))

    total = 0
    for cond in conds:
        total += sum(cfd[cond].values())

    x = random.randint(0, total)
    for cond in sorted(conds):
        x -= sum(cfd[cond].values())
        if x <= 0:
            return ' '.join(cond)


def get_users():
    """Creates a list of Slack display names.

    Returns:
        The list of names.
    """
    list_ = users_list()
    if not list_['ok']:
        return None

    users = []
    for member in list_['members']:
        if member['deleted']:
            continue

        if member['profile']['display_name']:
            users.append(member['profile']['display_name'])
        else:
            users.append(member['name'])

    return users


def word_tokenize(text):
    """Convenience wrapper around nltk.word_tokenize.

    Tokenizes the given string while also rewriting Slack-formatted text.

    Args:
        text: The string to tokenize.

    Returns:
        The tokenized string.
    """
    tokens = nltk.word_tokenize(text)

    i = 0
    modified = []
    while i < len(tokens):
        for j in range(min(4, len(tokens) - i), 1, -1):
            s = ''.join(tokens[i:i + j])
            if find(SPECIAL_PATTERN, s):
                modified.append(s)
                i += j - 1
                break
        else:
            modified.append(tokens[i])
        i += 1

    return modified
