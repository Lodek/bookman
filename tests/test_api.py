#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
import requests
from bookman.api import GoogleBooksApi
import json

class OpenLibApi():
    """
    Deprecated test suite
    """

    def setUp(self):
        self.api = OpenLibApi()
        self.isbn = '978-0123944245'

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

        
class TestGoogleBooksApi(TestCase):
    """
    """
    def setUp(self):
        self.api = GoogleBooksApi()
        self.isbn = '9780123944245'
        with open('test-json-google.json') as f:
            self.json_ref = json.load(f)

    def test_get_json(self):
        """Asserts the opebooks API hasn't changed and still sends the samestuff"""
        json_ref = self.json_ref['items'][0]['volumeInfo']
        j = self.api.get_json([self.isbn])[0]
        self.assertEqual(j, json_ref)
    
    def test_get_book(self):
        """Test the book is built correctly fetched from the API"""
        book = self.api.get_book(self.isbn)
        data = self.json_ref['items'][0]
        authors = data['volumeInfo']['authors']
        isbn = data['volumeInfo']['industryIdentifiers'][0]['identifier']
        publish_date = data['volumeInfo']['publishedDate']
        title = data['volumeInfo']['title']
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
