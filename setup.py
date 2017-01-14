from setuptools import setup, find_packages

setup(
    name='swapenv',
    author='Jackson Gilman',
    author_email='jackson.j.gilman@gmail.com',
    license='MIT',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'swapenv = swapenv.cli:main'
        ]
    },
    tests_require=['pytest', 'pytest-mock', 'pyhamcrest', 'pytest-cov'],
)
