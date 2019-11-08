#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from bookman.cli import Interface

class TestCLI(TestCase):
    """
    """
    def setUp(self):
        self.interface = Interface()

    def tearDown(self):
        pass

    def test_top_parser(self):
        """ """
        args = 'search wind isbn'.split()
        parsed = self.interface.top_parser(args)
        self.assertEqual(parsed.command, args[0])
        self.assertEqual(parsed.args, args[1:])

if __name__ == '__main__':
    main()
