#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import random
import re
from nltk import word_tokenize
from nltk.probability import ConditionalFreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.util import ngrams


def _capitalize(m):
    return ' '.join([c.upper() for c in m.groups()])


def _cond_samples(grams):
    for gram in grams:
        n = len(gram) - 1
        yield tuple([t.lower() for t in gram[:n]]), gram[n]


def _emote(tokens):
    i = 0
    modified = []
    pattern = '^:[^:]+:$'

    while i < len(tokens) - 2:
        for j in [3, 2, 1]:
            s = ''.join(tokens[i:i + j])
            if re.findall(pattern, s) or j == 1:
                i += j - 1
                modified.append(s)
                break
        i += 1

    while i < len(tokens):
        modified.append(tokens[i])
        i += 1

    return modified


def cfd(n, *fnames):
    tokens = []
    for fname in fnames:
        with open(fname, 'r') as f:
            tokens += _emote(word_tokenize(f.read()))

    grams = []
    for i in range(2, n + 1):
        grams += ngrams(tokens, i)
    return ConditionalFreqDist(_cond_samples(grams))


def discuss(topic, cfd, n, length, truncate):
    seed = topic.split(' ')
    original = list(seed)
    while len(seed) < length or seed[-1] not in ['.', '?', '!']:
        if len(seed) >= truncate:
            seed.append('...')
            break

        match = False

        dist = collections.defaultdict(int)
        for j in range(min(n, len(seed)), 0, -1):
            ngram = tuple([t.lower() for t in seed[-j:]])
            if ngram in cfd:
                for key, value in zip(cfd[ngram].keys(), cfd[ngram].values()):
                    if key == seed[-1]:
                        continue
                    dist[key] += value * j * j

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
    text = re.sub('(\s*)([.?!:,])(\s+)', r'\2 ', text)
    text = re.sub('^([a-z])', _capitalize, text)
    text = re.sub('([.?!]) ([a-z])', _capitalize, text)

    return text
