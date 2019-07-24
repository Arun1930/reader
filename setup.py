from setuptools import setup


package_name = 'reader'
filename = package_name + '.py'


def get_version():
    import ast

    with open(filename) as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=reader,
    version=,
    author='xyzinnovation',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid for attendance',
    url='https://github.com/Arun1930/reader.git',
    long_description=get_long_description(),
    py_modules=[package_name],
    entry_points={
        'console_scripts': [
            'reader = reader:main'
        ]
    },
    license='License :: OSI Approved :: MIT License',
)
