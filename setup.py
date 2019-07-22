import os

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

this = os.path.dirname(os.path.realpath(__file__))

def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()

def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()

    
setup(
    name='reader',
    version='0.1',
    author='Arun',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid reader for attendance',
    url='https://github.com/Arun1930/reader',
    long_description=readme,
    packages=['reader.py'],
    install_requires=read('requirements.txt'),
    py_modules=[package_name],
    scripts=['bin/reader'],
    license='License :: OSI Approved :: MIT License',
)
