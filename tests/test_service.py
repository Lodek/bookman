from unittest import TestCase, main
import logging

from bookman.model import Book
from bookman.service import *

def setup_logging():
    logfmt = '%(asctime)s %(name)s %(funcName)s %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logfmt,
                        filename='bookman.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logfmt)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

class TestSearchService(TestCase):

    def setUp(self):
        self.service = SearchService()
        self.items = {
            'title': 'harry potter',
            'authors': 'J.K. Rowling',
        }
        self.book = Book(**self.items)

    def test_book_contains_returns_true_when_all_attributes_exist(self):
        self.assertTrue(self.service.book_contains(self.book, **self.items))

    def test_book_contains_returns_true_when_attributes_exist(self):
        self.book.isbn = '10'
        self.assertTrue(self.service.book_contains(self.book, **self.items))

    def test_book_contains_returns_false_when_no_arg_exist(self):
        self.assertFalse(self.service.book_contains(self.book, isbn='10'))

    def test_book_search_matches_when_book_contains_all_keywords(self):
        query = 'harry rowling'
        self.assertTrue(self.service.book_search(self.book, query))

    def test_book_search_matches_when_book_doesnt_contains_all_keywords(self):
        query = 'harry rowling ree'
        self.assertFalse(self.service.book_search(self.book, query))
        
if __name__ == '__main__':
    setup_logging()
    main()
