"""
Module with book API classes that request book information from the web
"""
from googleapiclient.discovery import build
from bookman.model import Book

class ApiWrapper:
    """
    Wrapper for Google Books Api which does json processing and implements
    utility functions to be used directly with bookman's model objects.
    """
    API_NAME = 'books'
    API_VERSION = 'v1'

    def __init__(self, config):
        self.service = build(self.API_NAME, self.API_VERSION, developerKey=config.api_key)
        self.api = self.service.volumes()

    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        return [self.get_book(isbn) for isbn in isbns]

    def get_book(self, isbn):
        """Construct Book object from a single ISBN identifier, return book."""
        response = self._list_wrapper('', isbn=isbn)
        item = response['items'][0]
        return self.book_from_item(item)

    def _try_get(self, dict, key, default):
        """DRY function to try catch accessing value in dict, return default
        if value not key."""
        try:
            value = dict[key]
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
        try:
            identifiers = filter(lambda id: 'ISBN' in id['type'], volume_info['industryIdentifiers'])
            isbn = next(identifiers)['identifier']
        except KeyError:
            isbn = '0'
        except StopIteration:
            isbn = '0'
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book

    def _list_wrapper(self, query, **kwargs):
        keywords = ['intitle', 'inauthor', 'inpublisher',
                    'subject', 'isbn', 'lccn', 'oclc']
        for key in kwargs:
            if key not in keywords:
                raise AttributeError(f'kwargs must be one of {keywords}')
        keywords_query = self.keyword_query_builder(**kwargs)
        query = query.replace(' ', '+')
        query = query + keywords_query
        request = self.api.list(q=query)
        return request.execute()

    def query_books(self, q):
        """Query the api with the query string, return list of 10 Book objects
        that returned from query"""
        response = self._list_wrapper(q)
        items = response['items'][:10]
        books = [self.book_from_item(item) for item in items]
        return books

    def keyword_query_builder(self, **kwargs):
        """Builder method that receives kwargs and return a query string as
        specified by the Google Books documentation"""
        join_token = '+'
        assignment_token = ':'
        return join_token.join([f'{key}{assignment_token}{value}'
                                for key, value in kwargs.items()])
