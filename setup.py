#!/usr/bin/env python
# coding=utf-8
import os

from setuptools import setup

package_name = 'reader'
filename = package_name + '.py'

with open('README.md') as readme_file:
    readme = readme_file.read()

this = os.path.dirname(os.path.realpath(__file__))

def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''
    
setup(
    name=package_name,
    version='0.1',
    author='Arun',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid reader for attendance',
    url='https://github.com/Arun1930/reader',
    long_description=get_long_description(),
    install_requires=read('requirements.txt'),
    py_modules=[package_name],
    scripts:['bin/reader.py']
    license='License :: OSI Approved :: MIT License',
)
