import os
import sys
from setuptools import setup, find_packages


version = __import__('ii_deploytool').__version__

if sys.argv[-1] == 'publish': # upload to pypi
    os.system("python setup.py register sdist upload")
    print "You probably want to also tag the version now:"
    print " git tag -a %s -m 'version %s'" % (version, version)
    print " git push --tags"
    sys.exit()

setup(
    name='ii-deploytool',
    version=version,
    license='Apache License, Version 2.0',

    install_requires=[
        'Fabric==1.8.0',
    ],

    description='ideallical deploytool',
    long_description=open('README.rst').read(),

    author='Michael van de Waeter',
    author_email='info@ideallical.com',

    url='https://github.com/ideallical/ii-deploytool/',
    download_url='https://github.com/ideallical/ii-deploytool/zipball/master',

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
