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
        'delta': '10m ago',
        'href': '/fairylab/bar/',
        'info': 'Description of bar.'
    }, {
        'name': 'baz',
        'ok': False,
        'delta': '1h ago',
        'href': '/fairylab/baz/',
        'info': 'Description of baz.'
    }, {
        'name': 'foo',
        'ok': True,
        'delta': '2m ago',
        'href': '/fairylab/foo/',
        'info': 'Description of foo.'
    }],
    'internal': [{
        'name': 'quux',
        'ok': False,
        'delta': '15m ago',
        'href': '',
        'info': 'Description of quux.'
    }, {
        'name': 'quuz',
        'ok': True,
        'delta': '30s ago',
        'href': '',
        'info': 'Description of quuz.'
    }, {
        'name': 'qux',
        'ok': True,
        'delta': '2d ago',
        'href': '',
        'info': 'Description of qux.'
    }],
}
