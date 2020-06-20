"""
Module contains Controller definitions for bookman commands.
"""
from pathlib import Path
import subprocess
import inspect
import shutil
import sys
import re

from bookman.controller.abc import ControllerABC

class List(ControllerABC):
    """Lists all books in the library"""

    @property
    def command_name(self):
        return 'list'

    def parser_config(self):
        self.parser.add_argument('-f', '--format', default='isbn')

    def _controller(self, args):
        books = self.lib.books
        for book in books:
            print(getattr(book, args.format))


class Search(ControllerABC):
    """Search library for books"""

    @property
    def command_name(self):
        return 'search'

    def parser_config(self):
        self.parser.add_argument('pattern')
        self.parser.add_argument('-q', '--quiet', action='store_true',
                                 help='Quiet mode, prints only the ISBN')

    def _controller(self, args):
        books = self.lib.search(args.pattern)
        for book in books:
            s = book.isbn if args.quiet else str(book)
            print(s)



class Add(ControllerABC):
    """Receive a list of ISBN values, looks up the information about those books
    and add the books found to bookman."""

    @property
    def command_name(self):
        return 'add'

    def parser_config(self):
        help_msg = 'space separated isbns, use a - in the first position to read from stdin'
        self.parser.add_argument('isbns', nargs='+',
                                 help=help_msg)

    def _controller(self, args):
        isbns = sys.stdin if args.isbns[0] == '-' else args.isbns
        self.lib.add_books(isbns)
        self.lib.save()


class Open(ControllerABC):
    """Searches for books and call xdg-open on matches"""

    @property
    def command_name(self):
        return 'open'

    def parser_config(self):
        self.parser.add_argument('pattern')

    def _controller(self, args):
        books = self.lib.search(args.pattern)
        paths = self.lib.get_paths(books)
        for path in paths:
            subprocess.Popen(['zathura', str(path)], start_new_session=True)


class Dump(ControllerABC):
    """Write the book identified by the given ISBN to stdout"""
    @property
    def command_name(self):
        return 'dump'

    def parser_config(self):
        self.parser.add_argument('isbn')

    def _controller(self, args):
        books = self.lib.search(args.isbn)
        paths = self.lib.get_paths(books)
        with paths[0].open('rb') as f:
            sys.stdout.buffer.write(f.read())

class Migrate(ControllerABC):
    """Update books.json file to match the attributes in the book class"""
    @property
    def command_name(self):
        return 'migrate'

    def parser_config(self):
        pass

    def _controller(self, args):
        self.lib.save()



class AddFromFile(ControllerABC):
    """Take name of the specified file and queries google books with the name of the file.
    The top 5 matches will be returned and the user will asked which match
    matches the book being added. Adds the book based on the select match"""

    @property
    def command_name(self):
        return 'add_from_file'

    def parser_config(self):
        query_help = 'Query to be used in google books, if empty bookman will\
        generate a query based on the name of the given file'
        self.parser.add_argument('--query', help=query_help, default='')
        self.parser.add_argument('file')

    def _controller(self, args):
        p = Path(args.file)
        file_name = re.sub(r'\..*$', '', p.name)
        q = args.query if args.query else file_name
        results = self.lib.query_web(q)
        print('Select result that matches book being added')
        for i, book in enumerate(results):
            print(f'{i} - {str(book)}')
        choice = input('Input a number')
        try:
            index = int(choice)
        except ValueError:
            print(f'Error, {choice} is not a number in the allowed range. Exiting.',
                  file=sys.stderr)
            sys.exit()
        book = results[index]
        self.lib.add_books([book.isbn])
        self.lib.save()
        self._copy_book(book.isbn, args.file)

    def _copy_book(self, isbn, file_name):
        """ """
        p = Path(file_name)
        book = self.lib.search(isbn)[0]
        target = book.get_file_name() + p.suffix
        shutil.copy(file_name, self.lib.books_dir / target)

def get_commands(module_dict):
    """Generator that return all classes in this module that inherit from
    ControllerABC"""
    for obj in module_dict.values():
        if inspect.isclass(obj) and issubclass(obj, ControllerABC):
            try:
                yield obj()
            except TypeError:
                pass
