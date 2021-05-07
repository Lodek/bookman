"""
Models for bookman
"""


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

    def __str__(self):
        tags = "".join([f"[{tag}]" for tag in self.tags])
        return self.title
