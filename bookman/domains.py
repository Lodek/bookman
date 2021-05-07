"""
Domain functions for bookman
"""
from .models import Book


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
