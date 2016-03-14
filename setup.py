from setuptools import setup

__version__ = '0.1.0'

CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
]

setup(
    name='erudit-website-cli',
    version=__version__,
    author='Virgil Dupras',
    author_email='virgil.dupras@savoirfairelinux.com',
    packages=['erudit_website_cli'],
    url='https://github.com/erudit/erudit-website-cli',
    license='GPL',
    description="Scrape https://erudit.org for specified search results",
    classifiers=CLASSIFIERS,
    install_requires=[
        'requests<3.0',
        'beautifulsoup4<4.5',
        'tabulate<0.8',
    ],
    entry_points = {
        'console_scripts': [
            'erudit-website-cli = erudit_website_cli:main',
        ],
    },
)
