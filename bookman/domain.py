"""
Domain functions for bookman
"""
from .models import Book

# FIXME Use proper typehints

def item_to_book(item):
    # type: (dict) -> Book
    """
    Converter for `item` entity in Google Books' API response to
    Book model
    """
    pass

def books_from_response(response):
    # type: (dict) -> list(Book)
    """
    Convert reponse from API into list of `Book` entities
    """
    pass

def get_book_from_isbn(isbn):
    # type: str -> Book
    """Fetches `Book` from API using ISBN"""
    pass

def get_books_from_query(query):
    # type: str -> list(Book)
    """
    Return list of `Book` for each returned value fetched from the API
    """
    pass

def deserialize_book(filename):
    # type: str -> Book
    """
    Build Book based on the stringified format used by bookman
    """
    pass
