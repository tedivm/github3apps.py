# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


version = '0.2.2'
setup(

    name='github3apps.py',

    version=version,
    packages=find_packages(),

    description='Access the Github API as an Application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3',

    author='Robert Hafner',
    author_email='tedivm@tedivm.com',
    url='https://github.com/tedivm/github3apps.py',
    download_url="https://github.com/tedivm/github3apps.py/archive/v%s.tar.gz" % (version),
    keywords='automation github apps git',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',

        'Programming Language :: Python :: 3',
    ],

    install_requires=[
        'cryptography>=2.1.4,<3',
        'github3.py>=1,<2',
        'pyjwt>=1.5.3,<2',
        'requests>=2.18.0,<3',
    ],

    extras_require={
        'dev': [
            'pypandoc',
            'twine',
            'wheel'
        ],
    }
)
