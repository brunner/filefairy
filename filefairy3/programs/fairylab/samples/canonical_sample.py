#!/usr/bin/env python

sample = {
    'title':
    'home',
    'breadcrumbs': [{
        'href': '',
        'name': 'Home'
    }],
    'browsable': [{
        'name': 'bar',
        'ok': True,
        'new': False,
        'delta': '10m ago',
        'href': '/fairylab/bar/',
        'info': 'Description of bar.'
    }, {
        'name': 'baz',
        'ok': False,
        'new': False,
        'delta': '1h ago',
        'href': '/fairylab/baz/',
        'info': 'Description of baz.'
    }, {
        'name': 'foo',
        'ok': True,
        'new': True,
        'delta': '2m ago',
        'href': '/fairylab/foo/',
        'info': 'Description of foo.'
    }],
    'internal': [{
        'name': 'quux',
        'ok': False,
        'new': False,
        'delta': '15m ago',
        'href': '',
        'info': 'Description of quux.'
    }, {
        'name': 'quuz',
        'ok': True,
        'new': False,
        'delta': '30s ago',
        'href': '',
        'info': 'Description of quuz.'
    }, {
        'name': 'qux',
        'ok': True,
        'new': False,
        'delta': '2d ago',
        'href': '',
        'info': 'Description of qux.'
    }],
}
