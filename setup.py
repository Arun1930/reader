from setuptools import setup


package_name = 'reader'
p_n = 'reader'
p_n1 = 'mqtt-client'
p_n2 = 'antena-clear'
filename = 'reader' + '.py'


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=reader,
    version=0.1,
    author='xyzinnovation',
    author_email='arun.prasad@xyzinnotech.com',
    description='rfid for attendance',
    url='https://github.com/Arun1930/reader',
    long_description=get_long_description(),
    py_modules=[p_n,p_n1,p_n2],
    entry_points={
        'console_scripts': [
            'reader = p_n:main'
            'mqtt-client = p_n1:main'
            'antena-clear = p_n2:main'
        ]
    },
    license='License :: OSI Approved :: MIT License',
)
