"""
Models for bookman
"""
import re


# FIXME Use proper typehints
class Book:
    authors = []
    title = ''
    isbn = ''
    year = ''
    tags = []

    matcher = re.compile(r'(\d{4})(-\d{2}-\d{2})?')

    @classmethod
    def isbn_getter(cls, identifiers):
        filtered = filter(lambda id: 'ISBN' in id['type'], identifiers)
        mapped = map(lambda id: id['identifier'], filtered)
        return (['_'] + list(mapped)).pop()

    @classmethod
    def get_year(cls, date_str):
        return cls.matcher.search(date_str).groups(1)

    @classmethod
    def from_item(cls, item):
        """
        Converter for `item` entity in Google Books' API response to
        Book model
        """
        # type: dict -> Book
        obj = cls()
        info = item['volumeInfo']
        obj.title = info.get('title', 'untitled')
        obj.authors = info.get('authors', ['unknown'])
        if 'industryIdentifiers' in info:
            obj.isbn = cls.isbn_getter(info['industryIdentifiers'])
        else:
            obj.isbn = '_'
        date_str = info.get('publishedDate', '9999-01-01') 
        obj.year = cls.get_year(date_str)
        return obj

    def to_filename(self):
        # type: Book -> str
        """Build Book based on the stringified format used by bookman"""
        pass

    def __str__(self):
        tags = "".join([f"[{tag}]" for tag in self.tags])
        return self.title
