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

class Book:
    """
    Abstraction for a book
    """
    authors = []
    published_year = 0
    title = ''
    tags = []
    note = ''
    isbn = ''
    alises = []

    def to_json(self):
        """Serialize Book to a json"""
        pass

    def search(self, attr, exp, re=False):
        """Check whether exp is in the attr attribute of self."""
        pass

    @classmethod
    def from_api(cls, isbn):
        """Create Book object from a json fetched from an api"""
        pass

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
