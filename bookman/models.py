"""
Models for bookman
"""
from .utils import compose


# FIXME Use proper typehints
class Book:
    authors = []
    title = ''
    isbn = ''
    year = ''
    tags = []

    def to_filename(self):
        # type: Book -> str
        """Build Book based on the stringified format used by bookman"""
        pass

    def _format_authors(self):
        formatter = compose([
            sorted,
            lambda authors: authors if len(authors) <= 3 else authors[0] + ["EtAl"],
            lambda authors: ",".join(authors)
        ])
        authors = [author.replace(" ", "-") for author in self.authors]
        return formatter(authors)

    def _format_title(self):
        return "-".join(self.title.split(' '))

    def __str__(self):
        tags = "".join([f"[{tag}]" for tag in self.tags])
        authors = self._format_authors()
        title = self._format_title()
        fmt = f"{tags}{authors}_{title}({self.year})_{self.isbn}"
        return fmt
