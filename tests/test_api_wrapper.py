#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from bookman.api_wrapper import ApiWrapper

class TestApiWrapper(TestCase):
    """
    Simple integration tests / smoke tests for Api class
    """
    def setUp(self):
        self.wrapper = ApiWrapper()

    def tearDown(self):
        pass



if __name__ == '__main__':
    main()
