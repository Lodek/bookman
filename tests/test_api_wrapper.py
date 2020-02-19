#!/usr/bin/env python
"""

"""
from bookman.api_wrapper import ApiWrapper
from unittest.mock import MagicMock, Mock
from unittest import TestCase, main
from pathlib import Path
import json


class TestApiWrapper(TestCase):
    """
    Simple integration tests / smoke tests for Api class
    """
    test_folder = Path(__file__).expanduser().absolute().parent
    def setUp(self):
        self.api = MagicMock()
        self.wrapper = ApiWrapper(self.api)

    def get_assets_json(self, file_name):
        asset = self.test_folder / 'assets' / file_name
        with open(asset) as f:
            d = json.load(f)
        return d

    def tearDown(self):
        pass

    def test_get_book_returns_book_from_isbn(self):
        """
        Given an isbn
        When called get_book
        Then return should be a book
        """
        pass

    def test_book_from_item_parses_book_correctly(self):
        """
        Given an item dictionary from google books
        When book_from_item info is called
        Then return should be a book matching the dictionary
        """
        asset = 'google-books-item.json'
        item = self.get_assets_json(asset)
        book = self.wrapper.book_from_item(item)
        title = 'Introduction to Algorithms'
        authors = ['Thomas H. Cormen', 'Charles E. Leiserson',
                   'Ronald L. Rivest', 'Clifford Stein']
        isbn = '0262533057'
        self.assertEqual(book.title, title)
        self.assertEqual(book.authors, authors)
        self.assertEqual(book.isbn, isbn)

    def test_get_books_list_of_isbns_return_books(self):
        """
        Given list of isbns
        When book_from_isbns is called
        Then return should be a list of books matching the isbns
        """
        pass

    def test_query_book_query_return_list_of_books(self):
        """
        Given quuery string
        When called query_books
        Then return should be list of books for entries in the book results
        """
        #given
        asset = 'volumes_query.json'
        volumes = self.get_assets_json(asset)
        self.api.query_volumes = MagicMock(return_value=volumes)

        q = 'digital+design+harris'
        books = self.wrapper.query_books(q)
        
        self.assertEqual('Digital Design and Computer Architecture', books[0].title)
        self.assertEqual(len(books), 10)



if __name__ == '__main__':
    main()
