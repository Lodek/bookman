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
from bookman import OpenLibApi, Book
import json

class TestBook(TestCase):
    """
    Test the Book class
    """

    def setUp(self):
        self.book_d = dict(authors='a1 a2'.split(), title='title', publish_date=2010,
                      isbn='000000')
        self.book = Book(**self.book_d)

    def tearDown(self):
        pass

    def test_init(self):
        """Assert init method works accordingly"""
        book = Book(**self.book_d)
        self.assertEqual(book.authors, 'a1 a2'.split())
        self.assertEqual(book.title, 'title')
        self.assertEqual(book.publish_date, 2010)
        
        with self.assertRaises(AttributeError):
            self.book_d['invalid_attr'] = 'invalid'
            book = Book(**self.book_d)

    def test_serialize(self):
        """Assert serialize method generates the correct json"""
        t = dict(notes='', tags=[], aliases=[])
        t.update(self.book_d) #base dict
        #since dicts are unordered I can't make a direct comparassion of the
        #resulting strings cause ordering will be messed up.
        expected = json.loads(json.dumps(t))
        target = json.loads(self.book.to_json())
        self.assertEqual(expected, target)

    def test_unserialize(self):
        """Test the book is initialized correctly from a json"""
        j = self.book.to_json()
        d = json.loads(j)
        d['notes'] = 'test'
        book = Book(**d)
        self.assertEqual(book.authors, 'a1 a2'.split())
        self.assertEqual(book.title, 'title')
        self.assertEqual(book.publish_date, 2010)
        self.assertEqual(book.notes, 'test')
 
            

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

    def test_get_books(self):
        isbns = ['9780123944245', '9780756404741']
        books = self.api.get_books(isbns)
        self.assertEqual(len(books), 2)

        

if __name__ == '__main__':
    main()
