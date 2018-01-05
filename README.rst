C-Builder Project
=================


Purpose
-------
* To easily write C files
* It provides classes so you dont have to worry about maintaining indent, ending things with semi colong
* Make your C code standard if autogenerating using python script
* Can be used in following scenarios

    * Generating C code for your communication networks like CAN, LIN etc
    * Generation of code through other database networks

* It also includes a templating engine, that can produce a skeleton of python file that can generate the C code given
  as input

* So for example you want to start using this script for generating C code, you can follow the following steps

    * Generate a skeleton of the C code with example functions
    * Feed this as input to the parser as given below
    * This will generate a python file called <c_file_name>_gen.py
    * When this file is run it should produce a decent copy of the input file
    * Use this template python file either as a function to extend and connect the code to your database info

.. warning::

    The templating function is in beta mode


Installation
------------

This package can be pip installed

    pip install c_builder

.. note::

    Built and tested with python 3.6


Usage
-----

* For templating

    run_c_builder -i <input_c_file.c>

* For just writing to a c file

.. highlight:: python

    from c_builder import c_writer


* Then just use the file classes provided and check the documentation in the classes
* You can also check the generated template for pointers to usage
* Or check out the sample installed along with the library

For Bugs
--------

Join the slack workspace at -
https://join.slack.com/t/projectaja/shared_invite/enQtMjk1NTk0NzIwNDIzLWRmMTNjMzY3ZGFmYjY4MGZhOTBiNjZjZTA1YzM3MmFmYWIxOTJkY2QyOWNjM2JhZTk3NTMzMzNmZGIyZGM3NmY

And join the c_builder channel

Also you can email me at

pip[at]abhijit.bansal.com


Future
------

1. Add support for more C code
2. Support for doing standards check on the datatypes
3. More intelligent analysis
4. Support for C++
5. C++ style template classes for C


Version History
---------------

0.0.3 : Fix for package installation

0.0.2 : More support and documentation

0.0.1 : Initial version, tested upload to pypi




