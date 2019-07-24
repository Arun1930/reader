import os

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='reader',
    version='0.1',
    author='Arun',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid reader for attendance',
    url='https://github.com/Arun1930/reader',
    long_description=readme,
    scripts=['bin/reader'],
    license='License :: OSI Approved :: MIT License',
)
