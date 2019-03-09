from setuptools import (
    find_packages,
    setup,
)

config = {
    'name': 'testapp',
    'version': '0.0.1',
    'packages': find_packages(),
    'install_requires': ['snap-helpers'],
    'entry_points': {
        'console_scripts': [
            'service1 = testapp:service1',
            'service2 = testapp:service2'
        ],
        'snaphelpers.hooks': [
            'configure = testapp:configure_hook',
            'install = testapp:install_hook'
        ]
    },
}

setup(**config)
