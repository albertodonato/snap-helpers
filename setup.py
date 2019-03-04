from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)

tests_require = ['pytest']

config = {
    'name': 'snap-helpers',
    'version': '0.0.1',
    'license': 'LGPLv3+',
    'description': (
        'Helpers for interacting with the Snap system within a Snap'),
    'long_description': Path('README.rst').read_text(),
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://github.com/albertodonato/snap-helpers',
    'download_url': 'https://pypi.org/project/snap-helpers/#files',
    'packages': find_packages(include=['snaphelpers', 'snaphelpers.*']),
    'include_package_data': True,
    'entry_points': {
        'console_scripts': []
    },
    'test_suite': 'snaphelpers',
    'install_requires': ['packaging'],
    'tests_require': tests_require,
    'extras_require': {
        'testing': tests_require
    },
    'keywords': 'snap snappy snapcraft',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        (
            'License :: OSI Approved :: '
            'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Programming Language :: Python :: 3 :: Only'
    ]
}

setup(**config)
