"""
Title:
    Python script for the c_builder console

Author:
    Abhijit Bansal

"""

import argparse
import os
import sys
import logging

import c_builder
from c_builder import __version__ as versions

logger = c_builder.log.setup_console_logger('c_builder')


def parse_args():
    parser = argparse.ArgumentParser(description=('To read/write c_file'
                                                  'Tool version - {}'.format(versions.package_version)))

    parser.add_argument('-i', '--input_files', help='Input file or files(comma separated)', type=str)
    parser.add_argument('-o', '--output_dir', default='',
                        help='Output location, if not specified uses the same directory as input file(s)', type=str)

    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress all output')

    parser.add_argument('--verbose', type=int, default=20,
                        help='Verbosity levels - Default 10, 10-Debug, 20-Info, 30-Warning, 40-Error')

    parser.add_argument('--log-file', type=str, help='Path to logging file if needed')
    
    return parser.parse_args()


def header():
    logger.info('---------------------------------------------------------------------------')
    logger.info('--                       Starting c_builder                              --')
    logger.info('---------------------------------------------------------------------------')
    logger.info("C Builder Ver = {}".format(versions.package_version))


def footer():
    logger.info('---------------------------------------------------------------------------')
    logger.info('--                       Exiting c_builder                               --')
    logger.info('---------------------------------------------------------------------------')


def main():
    args = parse_args()

    # Set up logging
    c_builder.log.set_handler_level(logger, args.verbose)

    if args.quiet:
        c_builder.log.disable_handlers(logger)

    if args.log_file:
        if os.path.exists(os.path.dirname(args.log_file)):
            c_builder.log.setup_file_logger(args.log_file, logger.name, args.verbose)
        else:
            raise Exception("Parent directory for given logger file - {}, does not exist".format(args.log_file))

    # Now start the process
    input_files = args.input_files.split(',')

    output_dir = args.output_dir

    if output_dir:
        output_dir = output_dir.split(',')
        if len(output_dir) != len(input_files):
            raise ValueError("Incorrect number of input file and output directory given")
    else:
        output_dir = ['' for i in input_files]

    for file_path, output_dir in zip(input_files, output_dir):
        logger.info("Working on file - {}".format(file_path))
        c_builder.c_file_parser.parse_file(file_path, output_dir)
        logger.info("Result in - {}\n\n".format(output_dir))


if __name__ == '__main__':
    main()


