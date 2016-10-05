#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

__appname__ = "casino"
__author__ = "Vincent G. Guarnaccia (vguarnaccia)"
__email__ = "vincent.guarnaccia@gmail.com"
__version__ = "0.0.1"
__license__ = "GPL"

# for tips on logging go to
# http://docs.python-guide.org/en/latest/writing/logging/
LOGGER = logging.getLogger(__name__)

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description="Does a thing to some stuff.",
        epilog="As an alternative to the commandline, params can be placed in a file,"
        "one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
  # TODO Specify your real parameters here.
    parser.add_argument(
        "argument",
        help="pass ARG to the program",
        metavar="ARG")
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parser.parse_args()
    # Return all variable values
    return args

# Gather our code in a main() function

def main(args=None):
    """enters function"""
    if args is None:
        args = get_args()
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # TODO: Replace this with your actual code.

    # Setup logging
    logging.info("You passed an argument.")
    logging.debug("Your Argument: %s" % args.argument)

if __name__ == '__main__':
    main()
