#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from bookman.model import Book
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
 
       

if __name__ == '__main__':
    main()
