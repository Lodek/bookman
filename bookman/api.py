"""
Module with book API classes that request book information from the web
"""
import requests
from bookman.model import Book

class BookApi:
    """Base class that define a general interface for different information apis.
    The methods _construct_book() and get_json() are api specific and must
    be defined in the subclasses.
    The moethods get_book and get_books() leverage the common class interface
    to avoid repetition"""
    def get_json(self, isbns):
        """From a list of ISBNs, this method interacts with the api and return
        a list of jsons containing the books data."""
        pass

    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        json = self.get_json(isbns)
        books = [self._construct_book(data) for data in json]
        return books
            
    def get_book(self, isbn):
        """Construct Book object from a single ISBN identifier, return book."""
        book = self.get_books([isbn])[0]
        return book
               
    def _construct_book(self, data):
        """Data is a dict matching the json retrieved from the api,
        retrieve the desired information from dict and return Book object"""
        pass

class GoogleBooksApi(BookApi):
    """
    API class that interfaces with the Google Books API.
    """
    rest_html = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            self.rest_html += f'&key={api_key}'

    def get_json(self, isbns, processes=1):
        uris = [self.rest_html.format(isbn.replace('-', '')) for isbn in isbns]
        responses = [requests.get(uri) for uri in uris]
        jsons = [r.json() for r in responses]
        jsons = [json['items'][0]['volumeInfo'] for json in jsons]
        return jsons

    def _construct_book(self, data):
        title = data['title']
        authors = data['authors']
        publish_date = data['publishedDate']
        isbn = [d['identifier'] for d in data['industryIdentifiers'] if d['type'] == 'ISBN_13'][0]
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book


class OpenLibApi(BookApi):
    """
    API class, interfaces with the openlibrary API.
    DEPRECATED for now
    """
    request_url = 'https://openlibrary.org/api/books?&format=json&jscmd=data&bibkeys={}'
    def get_json(self, isbns):
        post_isbns = ['ISBN:'+isbn for isbn in isbns]
        url = self.request_url.format(','.join(post_isbns))
        r = requests.get(url)
        if r.status_code != 200:
            excep_msg = f'API Response error: response={r}, isbns={isbns}, url={url}'
            logger.info(excep_msg)
            raise RunTimeError(excep_msg)
        else:
            return r.json()

    def _construct_book(self, data):
        isbn = data['identifiers']['isbn_13'][0]
        authors = [author['name'] for author in data['authors']]
        date = data['publish_date']
        title = data['title']
        publish_date = data['publish_date']
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book