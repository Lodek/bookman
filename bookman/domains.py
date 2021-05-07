"""
Domain functions for bookman
"""
import functools
import re

from .models import Book


class Parser:
    """
    Parser for bookman file string
    """
    pass


class Domain:
    """
    Namespace with domain functions and instance of service to be used
    """

    def __init__(self, service):
        self.matcher = re.compile(r'(\d{4})(-\d{2}-\d{2})?')
        self.service = service

    def get_books_from_query(self, query):
        # type: str -> list(Book)
        """
        Return list of `Book` for each returned value fetched from the API
        """
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
        date_str = self.get_year(info)
        book.year = get_year(date_str)
        return obj

    def get_year(self, info):
        """Return year for book from info in API

        The `publishedDate` field from the API doesn't have a fixed 
        format. Some items only have a year, others have an ISO date.
        This func uses a regex to fetch only the year
        """
        date_str = info.get('publishedDate', '9999-01-01') 
        return self.matcher.search(date_str).groups(1)

    def clean_title(self, info):
        # type: dict -> str
        """This beauty of a function handles recovering the title from
        the `info` dict. The cleaned title should be formatted such that
        words start with a capital, there aren't any weird special
        characters and words are joined by '-'.
        """
        char_remover = lambda s: [c for c in s 
                                  if c not in "._-|\"`&~*"]
        space_trimmer = lambda s: re.sub(r" +", " ", s)
        funcs = [char_remover, space_trimmer, str.title,
                 str.trim, str.split, lambda xs: "-".join(xs)]

        title = info.get('title', 'Untitled')
        # The API sometimes returns this subtitle business
        # so we append it to title
        subtitle = info.get('subtitle', '')
        title = title + " " + subtitle

        return functools.reduce(lambda acc, f: f(acc), funcs, title)

    def clean_authors(self, info):
        # type: dict -> list(str)
        # TODO impl this
        return info.get('authors', ['unknown'])
        
    def isbn_getter(self, info):
        # type: dict -> str
        """
        Fetches ISBN from item, returns "-" if none is found
        """
        # Some items in Google books don't have the `industryIdentifiers`
        # field, so we add a default
        identifiers = info.get("industryIdentifiers", [])
        idenifiers.append({"ISBN_default": "-"})

        filtered = filter(lambda id: 'ISBN' in id['type'], identifiers)
        mapped = map(lambda id: id['identifier'], filtered)
        return max(mapped)
