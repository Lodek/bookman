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
import bookman.service as service

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


class Query(ControllerABC):
    """
    Query the books api with an arbitrary string, prints top results and asks user to pick
    one match. Add the chosen result to the local library.
    """

    @property
    def command_name(self):
        return 'query'

    def parser_config(self):
        self.parser.add_argument('query')

    def _controller(self, args):
        #TODO: Transfer query command to layer service as it will be used multiple
        #times in the code
        results = self.lib.query_web(args.query)
        print('Select result')
        for i, book in enumerate(results):
            print(f'{i} - {str(book)}')
        choice = input('Input a number: ')
        try:
            index = int(choice)
        except ValueError:
            sys.exit(f'Error, {choice} is not a number in the allowed range.')
        result = results[index]
        self.lib.add_books([result.isbn])
        book = self.lib.get(result.isbn)
        print(f'Added book: {book}')
        self.lib.save()
 

class Open(ControllerABC):
    """Searches for books and call xdg-open on matches"""

    #TODO Refactor open to recurssively search for files in directory that contain the given ISBN
    @property
    def command_name(self):
        return 'open'

    def parser_config(self):
        self.parser.add_argument('pattern')

    def _controller(self, args):
        books = self.lib.search(args.pattern)
        paths = service.find_books_in_dir(self.lib.books_dir, books)
        for path in paths:
            subprocess.Popen(['xdg-open', str(path)], start_new_session=True)


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

class Associate(ControllerABC):
    """
    Given a file, associate it to a book previously added to bookman.
    Association copies (or moves) the file to bookman's book directory.
    If a file name for the book isn't specified, bookman will use its default.
    NOTE: Bookman will *always* use the book's ISBN as a prefix for the inserted file.
    """
    @property
    def command_name(self):
        return 'associate'

    def parser_config(self):
        self.parser.add_argument('isbn',
                                 help='ISBN of a book in the library that will be used to name file')
        self.parser.add_argument('file', help='File to be copied over to bookmans book dir')
        self.parser.add_argument('--rm', action='store_true',
                                 help='Flag argument, set it if the source file should be removed')
        self.parser.add_argument('-n', '--name', help='')

    def _controller(self, args):
        book = self.lib.get(args.isbn)

        src = Path(args.file)

        target_name = args.name if args.name else service.generate_default_name(book)
        target_name = '{}-{}{}'.format(book.isbn, target_name, src.suffix)

        shutil_command = shutil.move if args.rm else shutil.copy2

        target = self.lib.books_dir / target_name
        
        shutil_command(args.file, target)



class AddFile(ControllerABC):
    """
    Given a query string and a file path, bookman will perform a query on the api
    using the given query string (if no query is given, bookman will use the file's
    name instead.
    The 5 first results will be printed and the user is asked to pick one, the
    chosen book will be added to the base.
    Finally, the file pointed by the given path will be copied to the books dir
    and will be associated to the new made entry.
    """
    @property
    def command_name(self):
        return 'add_file'

    def parser_config(self):
        query_help = 'Query to be used in google books, if empty bookman will\
        generate a query based on the name of the given file'
        self.parser.add_argument('file')
        self.parser.add_argument('--query', help=query_help, default='')
        self.parser.add_argument('-n', '--name', help='name for file in books dir')
        self.parser.add_argument('--rm', action='store_true',
                                 help='Flag argument, set it if the source file should be removed')

    def _controller(self, args):
        p = Path(args.file).expanduser()
        file_name = re.sub(r'\..*$', '', p.name)
        query = args.query if args.query else file_name
        results = self.lib.query_web(query)
        print('Select result that matches book being added')
        for i, book in enumerate(results):
            print(f'{i} - {str(book)}')
        choice = input('Input a number')
        try:
            index = int(choice)
        except ValueError:
            print(f'Error, {choice} is not a number in the allowed range.',
                  file=sys.stderr)
            sys.exit()
        result = results[index]
        self.lib.add_books([result.isbn])
        self.lib.save()

        book = self.lib.get(result.isbn)
        print(f'Added book: {book}')

        src = Path(args.file)

        target_name = args.name if args.name else service.generate_default_name(book)
        target_name = '{}-{}{}'.format(book.isbn, target_name, src.suffix)

        shutil_command = shutil.move if args.rm else shutil.copy2

        target = self.lib.books_dir / target_name
        
        shutil_command(args.file, target)


def get_commands(module_dict):
    """Generator that return all classes in this module that inherit from
    ControllerABC"""
    for obj in module_dict.values():
        if inspect.isclass(obj) and issubclass(obj, ControllerABC):
            try:
                yield obj()
            except TypeError:
                pass
