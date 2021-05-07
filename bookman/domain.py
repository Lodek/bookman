"""
Domain functions for bookman
"""
from datetime import date
import re

from .api_service import GBooksService

# FIXME Use proper typehints

class Book:
    authors = []
    title = ''
    isbn = ''
    year = ''
    tags = []

    matcher = re.compile(r'(\d{4})(-\d{2}-\d{2})?')

    @classmethod
    def isbn_getter(cls, identifiers):
        filtered = filter(lambda id: 'ISBN' in id['type'], identifiers)
        mapped = map(lambda id: id['identifier'], filtered)
        return (['_'] + list(mapped)).pop()

    @classmethod
    def get_year(cls, date_str):
        return cls.matcher.search(date_str).groups(1)

    @classmethod
    def from_item(cls, item):
        """
        Converter for `item` entity in Google Books' API response to
        Book model
        """
        # type: dict -> Book
        obj = cls()
        info = item['volumeInfo']
        obj.title = info.get('title', 'untitled')
        obj.authors = info.get('authors', ['unknown'])
        if 'industryIdentifiers' in info:
            obj.isbn = cls.isbn_getter(info['industryIdentifiers'])
        else:
            obj.isbn = '_'
        date_str = info.get('publishedDate', '9999-01-01') 
        obj.year = cls.get_year(date_str)
        return obj

    def to_filename(self):
        # type: Book -> str
        """Build Book based on the stringified format used by bookman"""
        pass

    def __str__(self):
        return self.title

class Parser:
    """
    Parser for bookman file string
    """
    pass

class Domain:
    """
    Namespace with domain functions and instance of service to be used
    """
    def __init__(self, service):
        self.service = service

    def get_books_from_query(self, query):
        # type: str -> list(Book)
        """
        Return list of `Book` for each returned value fetched from the API
        """
        results = self.service.query(query)
        return self.books_from_response(results)

    def books_from_response(self, response):
        # type: (dict) -> list(Book)
        """
        Convert reponse from API into list of `Book` entities
        """
        return [Book.from_item(item) for item in response['items']]

    def get_book_from_isbn(self, isbn):
        # type: str -> Book
        """Fetches `Book` from API using ISBN"""
        results = self.service.query('', isbn=isbn)
        return self.books_from_response(results)[0]
