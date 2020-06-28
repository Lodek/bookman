"""
"""

import configparser, json, re
from pathlib import Path

class Book:
    """
    Abstraction for a book
    """
    authors = []
    title = ''
    isbn = ''
    publish_date = ''
    tags = []
    notes = ''
    aliases = []

    @classmethod
    def inject_attributes(cls, attrs):
        """Receive dictionary whose items are going to be added as attributes
        to Book. The value for a key is set as the default value for the attr"""
        for key, value in attrs.items():
            setattr(cls, key, value)

    @classmethod
    def get_attrs(cls):
        names = set(dir(cls)) - set(dir(super()))
        function_type = type(cls._asdict)
        attrs = [name for name in names
                 if not hasattr(getattr(cls, name), '__call__')
                 and '__' not in name]
        return attrs
        

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __eq__(self, other):
        """Compare books based on their ISBN, if it matches they are equal"""
        return True if self.isbn == other.isbn else False

    def _asdict(self):
        """Serialize self to a dict"""
        return {attr : getattr(self, attr) for attr in self.get_attrs()}

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

    def __str__(self):
        return '\t'.join([self.title, ';'.join(self.authors), self.publish_date,
                          self.isbn, ','.join(self.tags), ','.join(self.aliases)])

    def get_file_name(self):
        """Generate a book's file name based on its attributes, return file name"""
        return self.isbn


class Lib:

    #TODO Decouple the API from Lib. Lib is a data layer object and should not depend
    #on the API. Transfer API dependent methods to the service layer.
    
    def __init__(self, books_dir, books_json, api):
        self.books_dir = Path(books_dir).expanduser().absolute()
        self.books_json = Path(books_json).expanduser().absolute()
        self.api = api
        self.books = []

    def get(self, isbn):
        """Return book with matching isbn"""
        return next(filter(lambda book: book.isbn == isbn, self.books))
        
    def get_paths(self, books):
        """Return list of path objects for book in books"""
        return [self.books_dir / f'{book.get_file_name()}.pdf' for book in books]
        
    def search(self, exp):
        """Iterate over list of books, search for the given text in the given attr, return list of matches"""
        return [book for book in self.books if book.search(exp)]

    def add_books(self, isbns):
        """From list of isbns and paths, add books to lib"""
        new_books = self.api.get_books(isbns)
        for book in new_books:
            if book not in self.books:
                self.books.append(book)

    def query_web(self, query):
        """ """
        return self.api.query_books(query)

    def load(self):
        try:
            with open(self.books_json) as f:
                books_raw = json.load(f)
                self.books = [Book(**book) for book in books_raw]
        except FileNotFoundError:
            self.books = []

    def save(self):
        books_asdict = [book._asdict() for book in self.books]
        with open(self.books_json, 'w') as f:
            json.dump(books_asdict, f, indent=4, sort_keys=True)

