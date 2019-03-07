from setuptools import (
    find_packages,
    setup,
)

config = {
    'name': 'testapp',
    'version': '0.0.1',
    'packages': find_packages(),
    'entry_points': {
        'snaphelpers.hooks': [
            'configure = testapp:configure_hook',
            'install = testapp:install_hook'
        ]
    },
}

setup(**config)
