#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for entertainment-related operations."""

import collections
import nltk.tokenize.treebank as treebank
import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/circus', '', _path))

from common.nltk_.nltk_ import word_tokenize  # noqa
from common.re_.re_ import search  # noqa

DECIDES = [
    '{}. Did you even need to ask?',
    'Definitely {}.',
    'It\'s {}, any day of the week.',
    'Easy, I prefer {}.',
    'I suppose {}, if I had to pick one.',
    'It\'s not ideal, but I\'ll go with {}.',
    '{}... I guess?',
    'That\'s a tough one. Maybe {}?',
]
WAFFLES = [
    'Neither seems like a good option to me.',
    'Why not both?',
]


def _capitalize(s):
    return s[0].upper() + s[1:]


def choose(options):
    """Choose one of the given options at random.

    Args:
        options: A list of options.

    Returns:
        A string indicating the choice.
    """
    statements = DECIDES + WAFFLES if len(options) == 2 else DECIDES
    statement = random.choice(statements)
    option = random.choice(options)

    return _capitalize(statement.format(option))


def discuss(topic, cfd, n, minimum, maximum):
    """Generates a nonsensical series of words given a topic and CFD.

    Args:
        topic: The topic phrase to seed the returned words.
        cfd: The conditional frequency distribution of words to reference.
        n: The order of N for the n-grams contained in the CFD.
        minimum: The minimum length of the desired word string.
        maximum: The maximum length of the desired word string.

    Returns:
        A series of words beginning with ``topic``, generated from the CFD.
    """
    if not topic:
        return None

    tokens = word_tokenize(topic)
    original = list(tokens)

    while len(tokens) < minimum or not search('[.?!]', tokens[-1]):
        if len(tokens) >= maximum:
            tokens.append('...')
            break

        dist = collections.defaultdict(int)
        for j in range(min(n, len(tokens)), 0, -1):
            ngram = tuple(t.lower() for t in tokens[-j:])
            if ngram in cfd:
                for key, value in cfd[ngram].items():
                    if key == tokens[-1]:
                        continue
                    dist[key] += value * j * j

        if tokens == original and '.' in dist.keys():
            dist.pop('.')

        x = random.randint(0, sum(dist.values()))
        for key, value in sorted(dist.items()):
            x -= value
            if x <= 0:
                tokens.append(key)
                break
        else:
            if tokens == original:
                return None
            tokens.append(random.choice(['and', 'but', 'for', 'or', 'so']))

    detokenizer = treebank.TreebankWordDetokenizer()
    reply = detokenizer.detokenize(tokens)

    sentences = []
    while search(r'[.?!:,]', reply):
        s, punctuation, reply = re.split(r'([.?!:,]+)', reply, 1)
        sentences.append(_capitalize(s.strip()) + punctuation)
    if search(r'\S', reply):
        sentences.append(_capitalize(reply.strip()))

    return ' '.join(sentences)


def who(names):
    statement = random.choice(DECIDES)
    name = random.choice(names)
    return statement.format(name)
