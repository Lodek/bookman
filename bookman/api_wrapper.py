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
    def __init__(self, api_key):
        self.api = Api(api_key)


    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        return [self.get_book(isbn) for isbn in isbns]

            
    def get_book(self, isbn):
        """Construct Book object from a single ISBN identifier, return book."""
        json = self.api.query_volumes_isbn(isbn)
        volume_info = json['items'][0]['volumeInfo']
        return self.book_from_info(volume_info)
               

    def book_from_info(self, volume_info):
        """volume_info is a dict matching a volumeInfo json retrieved from the api.
        Method process the JSON and return Book object"""
        volume_info = json['items'][0]['volumeInfo']
        title = volume_info['title']
        authors = volume_info['authors']
        publish_date = volume_info['publishedDate']
        isbn = [d['identifier'] for d in volume_info['industryIdentifiers'] if d['type'] == 'ISBN_13'][0]
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book

    def query_books(self, query):
        """Query the api with the query string, return list of 10 Book objects
        that returned from query"""
        json = self.api.query_volumes(query)
        volume_infos = json['items'][:10]
        books = [self.book_from_info(v) for v in volume_infos]
        return books
