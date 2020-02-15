#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from bookman.google_books import Api

class TestApi(TestCase):
    """
    Simple integration tests / smoke tests for Api class
    """
    def setUp(self):
        self.api = Api()

    def tearDown(self):
        pass

    def test_query_volumes_with_string(self):
        q = 'digital design computer architecture'
        json = self.api.query_volumes(q)
        self.assertGreater(json['totalItems'], 1)

    def test_query_volumes_isbn_return_volume(self):
        isbn = '0756404746'
        google_books_id = '2EounwEACAAJ'
        json = self.api.query_volumes_isbn(isbn)
        self.assertEqual(json['totalItems'], 1)
        self.assertEqual(json['items'][0]['id'], google_books_id)
        


if __name__ == '__main__':
    main()
