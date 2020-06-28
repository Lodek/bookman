"""
Service layer module
"""

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
