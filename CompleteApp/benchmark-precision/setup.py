#!/usr/bin/env python
"""Setup for the benchmarkdb module of Dft-Crossfilter.
"""

import subprocess
from setuptools import setup, find_packages
import os


setup(name='benchprec',
      version='0.1.0',
      description='Package for Benchmark Database',
      author='Joshua Gabriel',
      author_email='joshgabriel92@ufl.edu',
      packages=['precision'],
      package_data = {'precision':'*.R'}
      )
