from setuptools import setup
from os import path
import sys

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.join(here, "c_builder"))

import __version__ as version


def readme():
    with open('README.rst') as f:
        return f.read()


download_url = 'https://github.com/ajbansal/c_builder/archive/{}.tar.gz'.format(version.package_version)

setup(name='c_builder',
      version=version.package_version,
      long_description=readme(),
      test_suite='nose.collector',
      tests_require=['nose'],
      description='A tool to read write C file',
      url='https://github.com/ajbansal/c_builder',
      author='Abhijit Bansal',
      author_email='pip@abhijitbansal.com',
      license='MIT',
      packages=['c_builder', 'c_builder.tests'],
      scripts=['scripts/run_c_builder.py'],
      entry_points={'console_scripts': ['run_c_builder=run_c_builder:main']},
      package_data={"c_builder.tests": ['c_test.c']},
      zip_safe=False,
      install_requires=[],
      keywords=['testing c_builder C'],
      include_package_data=True,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Code Generators',
      ],
      )
