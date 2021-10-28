#!/usr/bin/env python
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read_requirements():
    with open('requirements.txt') as fp:
        return [row.strip() for row in fp if row.strip()]


about = {}
with open(os.path.join(here, 'mapilio_tools', '__init__.py'), 'r') as f:
    exec(f.read(), about)


setup(name='mapilio_tools',
      version=about['VERSION'],
      description='MAPILIO Image/Video Import Pipeline',
      url='https://github.com/mapilio/mapilio_tools',
      author='Visiosoft',
      license='BSD',
      python_requires='>=3.6',
      packages=['mapilio_tools', 'mapilio_tools.commands'],
      entry_points='''
      [console_scripts]
      mapilio_tools=mapilio_tools.__main__:main
      ''',
      install_requires=read_requirements(),
)
