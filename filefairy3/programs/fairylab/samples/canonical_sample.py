#!/usr/bin/env python

sample = {
    'title':
    'home',
    'breadcrumbs': [{
        'href': '',
        'name': 'Home'
    }],
    'browsable': [{
        'href': '/fairylab/bar/',
        'title': 'bar',
        'new': False,
        'info': 'Description of bar.',
        'table': [],
        'ts': '10m ago',
        'success': '',
        'danger': ''
    }, {
        'href': '/fairylab/baz/',
        'title': 'baz',
        'new': False,
        'info': 'Description of baz.',
        'table': [],
        'ts': '1h ago',
        'success': '',
        'danger': 'failed'
    }, {
        'href': '/fairylab/foo/',
        'title': 'foo',
        'new': True,
        'info': 'Description of foo.',
        'table': [],
        'ts': '2m ago',
        'success': '',
        'danger': ''
    }],
    'internal': [{
        'href': '',
        'title': 'quux',
        'new': False,
        'info': 'Description of quux.',
        'table': [],
        'ts': '15m ago',
        'success': '',
        'danger': 'failed'
    }, {
        'href': '',
        'title': 'quuz',
        'new': False,
        'info': 'Description of quuz.',
        'table': [],
        'ts': '30s ago',
        'success': 'just now',
        'danger': ''
    }, {
        'href': '',
        'title': 'qux',
        'new': False,
        'info': 'Description of qux.',
        'table': [],
        'ts': '2d ago',
        'success': '',
        'danger': ''
    }],
}
