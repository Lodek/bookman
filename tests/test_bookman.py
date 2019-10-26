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
        self.isbn = '978-0123944245'

    def tearDown(self):
        pass

    def test_get_json(self):
        """Asserts the opebooks API hasn't changed and still sends the samestuff"""
        with open('test-json.json') as f:
            json_stored = json.load(f)
        j = self.api.get_json([self.isbn])
        self.assertEqual(j, json_stored)
    
    def test_get_book(self):
        """Test the book is built correctly fetched from the API"""
        book = self.api.get_book(self.isbn)
        authors = ['David Money Harris']
        isbn = '9780123944245'
        publish_date = '2013'
        title = 'Digital design and computer architecture'
        self.assertEqual(book.title, title)
        self.assertEqual(book.authors, authors)
        self.assertEqual(book.isbn, isbn)
        self.assertEqual(book.publish_date, publish_date)
        

if __name__ == '__main__':
    main()
