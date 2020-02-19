"""
Module with book API classes that request book information from the web
"""
from bookman.model import Book
from bookman.google_books import Api


class ApiWrapper:
    """
    Wrapper for Google Books Api which does json processing and implements
    utility functions to be used directly with bookman's model objects.
    """
    def __init__(self, api):
        self.api = api


    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        return [self.get_book(isbn) for isbn in isbns]


    def get_book(self, isbn):
        """Construct Book object from a single ISBN identifier, return book."""
        json = self.api.query_volumes_isbn(isbn)
        item = json['items'][0]
        return self.book_from_item(item)

    def _try_get(self, d, key, default):
        """DRY function to try catch accessing value in dict, return default
        if value not key."""
        try:
            value = d[key]
        except KeyError:
            value = default
        return value

    def book_from_item(self, item):
        """item is a dict matching an item json retrieved from the api.
        Method process the JSON and return Book object.
        If book has no ISBN we doomed, or are we?"""
        volume_info = item['volumeInfo']
        title = self._try_get(volume_info, 'title', 'untitled')
        authors = self._try_get(volume_info, 'authors', ['unknown'])
        publish_date = self._try_get(volume_info, 'publishedDate', '1969-06-09')
        identifiers = filter(lambda id : 'ISBN' in id['type'], volume_info['industryIdentifiers'])
        try:
            isbn = next(identifiers)['identifier']
        except StopIteration:
            isbn = '039480001X'
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book

    def query_books(self, query):
        """Query the api with the query string, return list of 10 Book objects
        that returned from query"""
        json = self.api.query_volumes(query)
        items = json['items'][:10]
        books = [self.book_from_item(item) for item in items]
        return books
