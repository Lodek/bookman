"""
Service layer module
"""
from functools import reduce
import logging
import re

logger = logging.getLogger(__name__)

def generate_default_name(book):
    name = book.title.replace(' ', '_')
    return name

def find_books_in_dir(start, books):
    """Recurssively search for files that contain the one of the given isbns in
    their name. Return list of Paths that matched"""
    files = []
    dirs = []
    for p in start.iterdir():
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            dirs.append(p)
    while dirs:
        dir = dirs.pop()
        for p in dir.iterdir():
            if p.is_file():
                files.append(p)
            elif p.is_dir():
                dirs.append(p)       
    matches = [next(filter(lambda file: book.isbn in file.name, files))
               for book in books]
    return matches

def parse_string_properties(property_list):
    validator = re.compile(r'^([^=]+)=(.*)$')
    matches = [(p, validator.match(p)) for p in property_list]
    violations = filter(lambda match: not match[1], matches)
    error_msgs = [f'Property {violation} is invalid, must follow var=value.'
                      for violation in violations]
    if error_msgs:
        raise RuntimeError('\n'.join(error_msgs))
    return {match.group(1): match.group(2) for _, match in matches}

class SearchService:

    def get_book_keywords(self, book):
        attrs = book.get_attrs()
        items = {attr: getattr(book, attr) for attr in attrs}
        stringfy_list = lambda l: ' '.join(map(str, l))
        for key, value in items.items():
            if type(value) is list:
                items[key] = stringfy_list(value)
            else:
                items[key] = str(value)
        keywords = set(reduce(lambda a, b: f'{a} {b}', items.values(), '').split(' '))
        keywords = {word.lower() for word in keywords}
        logger.debug(f'keywords for book={book.isbn} keywords={keywords}')
        return keywords

    def search(self, lib, query, n=0, **kwargs):
        """Perform a search over the library using either a query string, which
        will return all matches that contain the given keywords in the string or through
        kwargs where the keys are attributes present in the book model."""
        logger.info(f'Searching lib for {query} and {kwargs}')
        if kwargs:
            result = [book for book in lib.books if self.book_contains(book, **kwargs)]
        else:
            result = [book for book in lib.books if self.book_search(book, query)]
        return result

    def book_search(self, book, query):
        logger.debug(f'Book search in {book}')
        query_words = [word.lower() for word in query.split(' ')]
        
        keywords = self.get_book_keywords(book)
        return all(map(lambda token: token in keywords, query_words))

    def book_contains(self, book, **kwargs):
        logger.debug(f'search book={book} for attrs={kwargs}')
        for key, value in kwargs.items():
            try:
                attr = getattr(book, key)
                if type(attr) is list and value not in attr:
                    return False
                elif attr != value:
                    return False
            except AttributeError:
                logger.warn(f'book model does not contain attr={key}')
                return False
        return True

