from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)

tests_require = ['pytest', 'pytest-mock']

config = {
    'name': 'snap-helpers',
    'version': '0.1.4',
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
        'console_scripts': [
            'snap-helpers = snaphelpers.scripts.snaphelpers:script',
            'snap-helpers-hook = snaphelpers.scripts.hook:script'
        ]
    },
    'test_suite': 'snaphelpers',
    'install_requires': ['packaging', 'PyYAML'],
    'tests_require': tests_require,
    'extras_require': {
        'testing': tests_require
    },
    'keywords': 'snap snappy snapcraft',
    'classifiers': [
        'Development Status :: 4 - Beta',
        (
            'License :: OSI Approved :: '
            'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Packaging'
    ]
}

setup(**config)
