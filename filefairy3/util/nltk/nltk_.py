#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import random
import re

from nltk import word_tokenize
from nltk.probability import ConditionalFreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.util import ngrams

_channel = '^<\#\w+\|\w+>$'
_user = '^<@\w+>$'
_case_pattern = '|'.join([_channel, _user])
_fix_pattern = '|'.join(['^:[^:]+:$', _channel, _user])


def _case(grams):
    return [t if re.findall(_case_pattern, t) else t.lower() for t in grams]


def _capitalize(m):
    return ' '.join([c.upper() for c in m.groups()])


def _cond_samples(grams):
    for gram in grams:
        n = len(gram) - 1
        yield tuple(_case(gram[:n])), gram[n]


def _fix(tokens):
    i = 0
    modified = []

    while i < len(tokens):
        for j in range(min(4, len(tokens) - i), 0, -1):
            s = ''.join(tokens[i:i + j])
            if re.findall(_fix_pattern, s) or j == 1:
                i += j - 1
                modified.append(s)
                break
        i += 1

    return modified


def cfd(n, *fnames):
    tokens = []
    for fname in fnames:
        with open(fname, 'r') as f:
            tokens += _fix(word_tokenize(f.read()))

    grams = []
    for i in range(2, n + 1):
        grams += ngrams(tokens, i)
    return ConditionalFreqDist(_cond_samples(grams))


def discuss(topic, cfd, n, length, truncate):
    seed = _fix(word_tokenize(topic))
    original = list(seed)
    while len(seed) < length or seed[-1] not in ['.', '?', '!']:
        if len(seed) >= truncate:
            seed.append('...')
            break

        match = False

        dist = collections.defaultdict(int)
        for j in range(min(n, len(seed)), 0, -1):
            ngram = tuple(_case(seed[-j:]))
            if ngram in cfd:
                for key, value in zip(cfd[ngram].keys(), cfd[ngram].values()):
                    if key == seed[-1]:
                        continue
                    dist[key] += value * j * j

        if seed == original and len(dist.keys()) > 1 and '.' in dist.keys():
            dist.pop('.')

        x = random.randint(0, sum(dist.values()))
        for key, value in dist.iteritems():
            x -= value
            if x <= 0:
                seed.append(key)
                match = True
                break

        if not match:
            if seed == original:
                return 'I don\'t know anything about ' + topic + '.'
            conjunction = random.choice(['and', 'but', 'for', 'or', 'so'])
            seed.append(conjunction)

    detokenizer = TreebankWordDetokenizer()
    text = detokenizer.detokenize(seed)
    text = re.sub('(\s+)(\.+)(\s*)', r'\2\3', text)
    text = re.sub('(\.+)\.([^.\s])', r'\1. \2', text)
    text = re.sub('(\s+)([@#])(\s*)', r' \2 ', text)
    text = re.sub('(\s*)([.?!:,])(\s+)', r'\2 ', text)
    text = re.sub('^([a-z])', _capitalize, text)
    text = re.sub('([.?!]) ([a-z])', _capitalize, text)

    return text


def imitate(cfd, n, length, truncate):
    conditions = cfd.conditions()
    total = 0
    for condition in conditions:
        total += sum(cfd[condition].values())

    x = random.randint(0, total)
    for condition in conditions:
        x -= sum(cfd[condition].values())
        if x <= 0 and re.findall('^\w', condition[0]):
            return discuss(' '.join(condition), cfd, n, length, truncate)

    return ''
