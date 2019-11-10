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

import configparser, json, re
from pathlib import Path

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
        self.file_name = ''
        for attr, value in kwargs.items():
            try:
                getattr(self, attr)
                setattr(self, attr, value)
            except AttributeError:
                raise AttributeError(f'Invalid attr {attr}.')

    def __eq__(self, other):
        """Compare books based on their ISBN, if it matches they are equal"""
        return True if self.isbn == other.isbn else False

    def _asdict(self):
        """Serialize self to a dict"""
        attrs = 'authors title isbn publish_date tags notes aliases'.split()
        return {attr : getattr(self, attr) for attr in attrs}

    def to_json(self):
        """Serialize Book to a json"""
        return json.dumps(self._asdict())

    def search(self, exp, re=False):
        """Check whether exp is in the attr attribute of self."""
        tags_str = ','.join(self.tags)
        aliases_str = ','.join(self.aliases)
        authors_str = ','.join(self.authors)
        s = self.title + authors_str + self.notes + aliases_str + self.isbn + tags_str
        return True if exp.lower() in s.lower() else False

    def __repr__(self):
        s = '{}: title={}; authors={}; isbn={};'
        return s.format(self.__class__, self.title, self.authors, self.isbn)

class Lib:
    
    def __init__(self, books_dir, books_data, api_key, api):
        self.books_dir = Path(books_dir).expanduser().absolute()
        self.books_data = Path(books_data).expanduser().absolute()
        self.api_key = api_key
        self.api = api(api_key)
        self.books = []
        
    
    def get_paths(self, books):
        """Return list of path objects for book in books"""
        return [self.books_dir / f'{book.isbn}.pdf' for book in books]
        
    def search(self, exp):
        """Iterate over list of books, search for the given text in the given attr, return list of matches"""
        return [book for book in self.books if book.search(exp)]

    def add_books(self, isbns):
        """From list of isbns and paths, add books to lib"""
        new_books = self.api.get_books(isbns)
        for book in new_books:
            if book not in self.books:
                self.books.append(book)

    def load(self):
        try:
            with open(self.books_data) as f:
                books_raw = json.load(f)
                self.books = [Book(**book) for book in books_raw]
        except FileNotFoundError:
            self.books = []

    def save(self):
        books_asdict = [book._asdict() for book in self.books]
        with open(self.books_data, 'w') as f:
            json.dump(books_asdict, f, indent=4, sort_keys=True)

