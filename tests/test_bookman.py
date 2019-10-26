#!/usr/bin/env python
"""

"""
from pathlib import Path
p = Path(__file__).parent
p = (p.parent.absolute().parent) / 'bookman'
import sys
sys.path.insert(0, str(p))

from unittest import TestCase, main
import requests
from bookman import OpenLibApi
import json

class TestBook(TestCase):
    """
    Test the Book class
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestOpenLibApi(TestCase):
    """
    """
    def setUp(self):
        self.api = OpenLibApi()

    def tearDown(self):
        pass

    def test_api_change(self):
        """Asserts the opebooks API hasn't changed and still sends the samestuff"""
        isbn = '978-0123944245'
        with open('test-json.json') as f:
            json_stored = json.load(f)
        j = self.api.fetch_book(isbn)
        self.assertEqual(j, json_stored)
    

        

if __name__ == '__main__':
    main()
