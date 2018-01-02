from setuptools import setup
from os import path
import sys

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.join(here, "c_builder"))

import __version__ as version

download_url = 'https://github.com/ajbansal/c_builder/archive/{}.tar.gz'.format(version.package_version)

setup(name='c_builder',
      version=version.package_version,
      description='A tool to read write C file',
      url='https://github.com/ajbansal/c_builder',
      author='Abhijit Bansal',
      author_email='pip@abhijitbansal.com',
      license='MIT',
      packages=['c_builder'],
      scripts=[],
      # entry_points={'console_scripts': ['c_templater=c_builder:c_file_parser:main']},
      package_data={"c_builder": []},
      zip_safe=False,
      install_requires=[],
      keywords=['testing', 'c_builder', 'C'],
      classifiers=[]
      )
