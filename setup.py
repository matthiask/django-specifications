#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-specifications',
    version=__import__('specifications').__version__,
    description='Additional, dynamic fields for all Django models.',
    long_description=read('README.rst'),
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='http://github.com/matthiask/django-specifications/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(),
    package_data={
        '': ['*.html', '*.txt'],
        'specifications': [
            'locale/*/*/*.*',
            # 'static/specifications/*.*',
            # 'static/specifications/*/*.*',
            'templates/*.*',
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*',
        ],
    },
    install_requires=[
        'Django>=1.4.2',
    ],
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
)
