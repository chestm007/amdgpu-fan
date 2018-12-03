import os
import time
from distutils.core import setup

from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

VERSION = os.environ.get('TRAVIS_TAG') or '0.0.0-{}'.format(time.time())

setup(
    name='amdgpu_fan',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/chestm007/amdgpu_fan',
    license='GPL-2.0',
    author='Max Chesterfield',
    author_email='chestm007@hotmail.com',
    maintainer='Max Chesterfield',
    maintainer_email='chestm007@hotmail.com',
    description='amdgpu fan controller',
    long_description=readme,
    install_requires=[
    ],
    entry_points="""
        [console_scripts]
        amdgpu-fan=amdgpu_fan.controller:main
    """,
)
