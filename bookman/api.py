"""
Module with book API classes that request book information from the web
"""
from bookman.model import Book
from google_books import Api


class GBooksWrapper:
    """
    Wrapper for Google Books Api which does json processing and implements
    utility functions to be used directly with bookman's model domain.
    """
    def __init__(self, api_key=''):
        self.api = Api(api_key)


    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        return [self.get_book(isbn) for isbn in isbns]

            
    def get_book(self, isbn):
        """Construct Book object from a single ISBN identifier, return book."""
        json = self.api.query_volumes_isbn(isbn)
        return self.construct_book(json)
               

    def construct_book(self, json):
        """Json is a dict matching the json retrieved from the api,
        retrieve the desired information from dict and return Book object"""
        volume_info = json['items'][0]['volumeInfo']
        title = volume_info['title']
        authors = volume_info['authors']
        publish_date = volume_info['publishedDate']
        isbn = [d['identifier'] for d in volume_info['industryIdentifiers'] if d['type'] == 'ISBN_13'][0]
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book
