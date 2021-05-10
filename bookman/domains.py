"""
Domain functions for bookman
"""
import re
from pathlib import Path
from functools import reduce

from .models import Book
from .utils import compose
from bookman import settings

condense_space = lambda s: re.sub(r" +", " ", s)

def pascal_to_space(name):
    # type: str -> str
    """
    Transforms a PascalCase string into space separated
    eg. FooBar -> Foo Bar
    """
    space_prepend = lambda c: c if c.islower() else " " + c
    name = reduce(lambda acc, c: acc + space_prepend(c), name, "")
    return name.strip()


class Parser:
    """
    Logic related to deseralizing bookman's format into model instances
    """
    pass


class ApiDomain:
    """
    Logic mapping API to model domain
    """

    def __init__(self, service):
        self.matcher = re.compile(r'(\d{4})(-\d{2}-\d{2})?')
        self.service = service

    def get_books_from_query(self, query):
        # type: str -> list(Book)
        """
        Return list of `Book` for each returned value fetched from the API
        """
        query = self._clean_query(query)
        results = self.service.query(query)
        return self.books_from_response(results)

    def books_from_response(self, response):
        # type: (dict) -> list(Book)
        """
        Convert reponse from API into list of `Book` entities
        """
        return [self.from_item(item) for item in response['items']]

    def get_book_from_isbn(self, isbn):
        # type: str -> Book
        """Fetches `Book` from API using ISBN"""
        results = self.service.query('', isbn=isbn)
        return self.books_from_response(results)[0]

    def from_item(self, item):
        # type: dict -> Book
        """
        Converter for `item` entity in Google Books' API response to
        Book model
        """
        book = Book()
        info = item['volumeInfo']
        book.title = self.clean_title(info)
        book.authors = self.clean_authors(info)
        book.isbn = self.isbn_getter(info)
        book.year = self.get_year(info)
        return book

    def get_year(self, info):
        """Return year for book from info in API
        """
        # The `publishedDate` field from the API doesn't have a fixed 
        # format. Some items only have a year, others have an ISO date.
        # So we use a regex to fetch only the year
        date_str = info.get('publishedDate', '9999-01-01') 
        return self.matcher.search(date_str).group(1)

    def clean_title(self, info):
        # type: dict -> str
        """
        Return book title such that each word starts with a capital.
        Also strips symbols from title
        eg: Sample title & another info -> Sample Title Another Info
        """
        formatter = compose([
            lambda s: "".join([c for c in s if c not in "._-|\"`&~*,:"]),
            lambda s: re.sub(r" +", " ", s),
            str.title,
            str.strip
        ])

        title = info.get('title', 'Untitled')
        # The API sometimes returns this subtitle business
        # so we append it to title
        subtitle = info.get('subtitle', '')
        title = title + " " + subtitle

        return formatter(title)

    def clean_authors(self, info):
        # type: dict -> list(str)
        """
        Performs some preprocessing over the authors to format
        them in a regular way.
        Removes preios and other symbols from author name.
        Return list of strings, author name and surname is space 
        separated
        """
        author_processor = compose([
            lambda s: re.sub(r"\.|,|\&", " ", s),
            lambda s: re.sub(r" +", " ", s),
            str.title,
        ])

        authors = info.get("authors", ["Unknown"])
        return list(map(author_processor, authors))
        
    def isbn_getter(self, info):
        # type: dict -> str
        """
        Fetches ISBN from item, returns "" if none is found
        """
        # Some items in Google books don't have the `industryIdentifiers`
        # field, so we add a default
        identifiers = info.get("industryIdentifiers", [])
        identifiers.append({"type": "ISBN_default", "identifier": ""})

        filtered = filter(lambda id: 'ISBN' in id['type'], identifiers)
        mapped = map(lambda id: id['identifier'], filtered)
        return max(mapped)

    def _clean_query(self, query):
        """
        Given query string, perform transform it to remove certain 
        characters, remove double space with the intent of improving
        API matching odds.
        """
        char_transform = lambda c: c if c not in "_-&.,()[]" else " "
        f = compose((
            lambda s: "".join(list(map(char_transform, s))),
            condense_space, str.lower))
        return f(query)


class FileSystemDomain:
    """
    Logic to handle File system related operations
    """

    def filename_from_path(self, path):
        # type: (str|Path) -> str
        """
        From a filesystem path or a Path object, return the 
        name of the file, without its suffix.
        """
        return Path(str(path)).stem

    def get_bookman_path(self):
        return Path(settings.DIR).expanduser().resolve()
