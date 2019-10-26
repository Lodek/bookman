"""
ok, what do I want?
a simple book organizer app
insert book through file, isbn
keeps all books in a book directory
book alias
open book by alias
fetch book metadata through web api

why do I want/need?
Calibre is a pain.
is it tho?
a lil bit.
i don't hate it but it has more than I need and it doesn't solve the thing that I want. i'd like my shit to be scriptable.
so the question is, do you ACTUALLY need this? cause it's gonna cost time.
overall I think it's a 'would be nice' situation because my books are pretty damn messy rn tbh.

FINE.
Just do it then.

How are you doing searchs tho?
I'd need to make a nice cli for it.
with options.
or maybe scriptable.
idk honestly.
for now i could consider searching the json file
eventually i'd have to add a proper cli to it.

moreover, i feel like this would be a good template for my bookmarks and mellori
i wrote bookpoint but i never used it, never even got around to organizing those darn favorites' """

import requests
import configparser, json, re

class Book:
    """
    Abstraction for a book
    """
    def __init__(self, authors, title, isbn, publish_date, **kwargs):
        self.authors = authors
        self.title = title
        self.isbn = isbn
        self.publish_date = publish_date
        self.tags = []
        self.notes = ''
        self.aliases = []
        for attr, value in kwargs.items():
            try:
                getattr(self, attr)
                setattr(self, attr, value)
            except AttributeError:
                raise AttributeError(f'Invalid attr {attr}.')

    def _asdict(self):
        """Serialize self to a dict"""
        attrs = 'authors title isbn publish_date tags notes aliases'.split()
        return {attr : getattr(self, attr) for attr in attrs}

    def to_json(self):
        """Serialize Book to a json"""
        return json.dumps(self._asdict())

    def search(self, attr, exp, re=False):
        """Check whether exp is in the attr attribute of self."""
        pass

    def __repr__(self):
        s = '{}: title={}; authors={}; isbn={};'
        return s.format(self.__class__, self.title, self.authors, self.isbn)
        

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


class Lib:
    
    def __init__(self, config_path='~/.bookmanrc'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.books_dir = self.config['bookman']['books_dir']
        self.books_data = self.config['bookman']['books_data']
        #self.api = GoogleBooksApi(self.config['bookman']['api_key'])
        self.api = GoogleBooksApi()
        self.books = []
    
    def find_books(self, attr, text):
        """Iterate over list of books, search for the given text in the given attr, return list of matches"""
        pass

    def add_books(self, isbns):
        """From list of isbns and paths, add books to lib"""
        new_books = self.api.get_books(isbns)
        self.books.extend(new_books)

    def load_lib():
        with open(self.books_data) as f:
            books_raw = json.load(f)
        self.books = [Book(**book) for book in books_raw]

    def save_lib():
        books_asdict = [book._asdict() for book in self.books]
        with open(self.books_data) as f:
            json.dump(books_asdict, f)

def main():
    isbns = ['978-1886529236', '0615880991']
    lib = Lib('config.ini')
    lib.add_books(isbns)
    print(lib.books)

    

if __name__ == '__main__':
    main()
