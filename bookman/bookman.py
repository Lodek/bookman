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
import re

class Book:
    """
    Abstraction for a book
    """
    def __init__(self, authors, title, isbn, publish_date):
        self.authors = authors
        self.title = title
        self.isbn = isbn
        self.publish_date = publish_date
        self.tags = []
        self.note = ''
        self.aliases = []

    def to_json(self):
        """Serialize Book to a json"""
        pass

    def search(self, attr, exp, re=False):
        """Check whether exp is in the attr attribute of self."""
        pass

    def __repr__(self):
        s = '{}: title={}; authors={}; isbn={};'
        return s.format(self.__class__, self.title, self.authors, self.isbn)
        

class OpenLibApi:
    """
    API class, interfaces with the openlibrary API.
    """

    request_url = 'https://openlibrary.org/api/books?&format=json&jscmd=data&bibkeys={}'

    def get_json(self, isbns):
        """Construct the GET url for the openlib api. The url contains all isbns
        in the given list. Expect isbns to be a list. Return request json"""
        post_isbns = ['ISBN:'+isbn for isbn in isbns]
        url = self.request_url.format(','.join(post_isbns))
        r = requests.get(url)
        if r.status_code != 200:
            excep_msg = f'API Response error: response={r}, isbns={isbns}, url={url}'
            logger.info(excep_msg)
            raise RunTimeError(excep_msg)
        else:
            return r.json()

    def get_books(self, isbns):
        """Construct Book objects from a list of isbns, return list of books"""
        json = self.get_json(isbns)
        books = [self._construct_book(data) for data in json.values()]
        return books
            
    def get_book(self, isbn):
        """Run request to fetch data for ISBN, return book object"""
        json = self.get_json([isbn])
        data = list(json.values())[0]
        return self._construct_book(data)
            
    def _construct_book(self, data):
        """Return Book Object from the fetched json data"""
        isbn = data['identifiers']['isbn_13'][0]
        authors = [author['name'] for author in data['authors']]
        date = data['publish_date']
        title = data['title']
        publish_date = data['publish_date']
        book = Book(authors=authors, title=title, isbn=isbn, publish_date=publish_date)
        return book


class Lib:
    
    books = []
    books_dir = ''
    books_data = ''
    
    def find_books(self, attr, text):
        """Iterate over list of books, search for the given text in the given attr, return list of matches"""
        pass

    def add_books(self, isbns, paths, processes=2):
        """From list of isbns and paths, add books to lib"""
        pass

    def load_lib():
        pass

    def save_lib():
        pass
