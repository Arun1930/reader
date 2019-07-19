from setuptools import setup


package_name = 'reader'
filename = package_name + '.py'

def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name=package_name,
    version=get_version(),
    author='Arun',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid reader for attendance',
    url='https://github.com/Arun1930/reader',
    long_description=get_long_description(),
    py_modules=[package_name],
    entry_points={
        'console_scripts': [
            'reader = reader:main'
        ]
    },
    license='License :: OSI Approved :: MIT License',
)