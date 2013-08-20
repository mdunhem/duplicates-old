#!/usr/bin/env python
""":mod:`duplicates.main` -- Program entry point
"""
from __future__ import print_function

import sys
import options
import controller


def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """

    option = options.Options(argv)
    duplicatesController = controller.Controller(option)

    duplicatesController.run()

    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
