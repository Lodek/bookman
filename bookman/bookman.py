import subprocess, configparser, argparse, shutil, sys, os, re
from bookman.api_wrapper import ApiWrapper
from bookman.google_books import Api
from bookman.model import Lib
from pathlib import Path

class Command:
    """
    Class for cli functions of bookman
    """

    choices = 'dump search add list open add_from_file'.split()

    def __init__(self, lib):
        self.lib = lib

    @classmethod
    def call(cls, lib, args):
        """Router that invokes the correct method"""
        obj = cls(lib)
        f = getattr(obj, args.command)
        f(args.args)

    
    def search(self, top_args):
        """Search library for books"""
        parser = argparse.ArgumentParser(description=self.search.__doc__)
        parser.add_argument('pattern')
        parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode, prints only the ISBN')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.pattern)
        for book in books:
            s = book.isbn if args.quiet else str(book)
            print(s)

    
    def list(self, top_args):
        """Lists all books in the library"""
        parser = argparse.ArgumentParser(description=self.list.__doc__)
        parser.add_argument('-f', '--format', default='isbn')
        args = parser.parse_args(top_args)
        books = self.lib.books
        for book in books:
            print(getattr(book, args.format))

    
    def add(self, top_args):
        """Receive a list of ISBN values, looks up the information about those books
        and add the books found to bookman."""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('isbns', nargs='+', help='space separated isbns, use a - in the first position to read from stdin')
        args = parser.parse_args(top_args)
        isbns = sys.stdin if args.isbns[0] == '-' else args.isbns
        self.lib.add_books(isbns)
        self.lib.save()


    
    def open(self, top_args):
        """Searches for books and call xdg-open on matches"""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('pattern')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.pattern)
        paths = self.lib.get_paths(books)
        for path in paths:
            subprocess.Popen(['zathura', str(path)], start_new_session=True)

    
    def dump(self, top_args):
        """Write the book identified by the given ISBN to stdout"""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('isbn')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.isbn)
        paths = self.lib.get_paths(books)
        with paths[0].open('rb') as f:
            sys.stdout.buffer.write(f.read())

    def add_from_file(self, top_args):
        """Take name of the specified file and queries google books with the name of the file.
        The top 5 matches will be returned and the user will asked which match
        matches the book being added. Adds the book based on the select match"""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('file')
        query_help = 'Query to be used in google books, if empty bookman will\
        generate a query based on the name of the given file'
        parser.add_argument('--query', help=query_help, default='')
        args = parser.parse_args(top_args)
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
            exit()
        book = results[index]
        self.lib.add_books([book.isbn])
        self.lib.save()
        self.copy_book(book.isbn, args.file)

    def copy_book(self, isbn, file_name):
        """ """
        p = Path(file_name)
        book = self.lib.search(isbn)[0]
        target = book.get_file_name() + p.suffix
        shutil.copy(file_name, self.lib.books_dir / target)
        


class Interface:
    """
    Initial parser for bookman.
    Sequentially source the configuration variables, parses the top lvl args
    and routes the arguments to the appropriate command.
    """
    def __init__(self):
        self.attributes = 'books_json api_key books_dir'.split()
        self.lib_attrs = {attr : '' for attr in self.attributes}

    @classmethod
    def do(cls):
        """Parse command line arguments, initialize and load Lib, route
        command to Command class"""
        self = cls()
        args = self.parse()
        self.load_ini(args)
        self.load_env()
        self.config_from_args(args)
        api = Api(self.lib_attrs['api_key'])
        wrapper = ApiWrapper(api)
        lib = Lib(api=wrapper, books_json=self.lib_attrs['books_json'], books_dir=self.lib_attrs['books_dir'])
        lib.load()
        Command.call(lib, args)

    def parse(self, args=sys.argv):
        """Parser for the top level arguments."""
        args = args[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument('command', choices=Command.choices)
        parser.add_argument('args', nargs=argparse.REMAINDER)
        parser.add_argument('-c', '--config', default='~/.bookman.ini', help='bookman config file')
        parser.add_argument('-f', '--books_json', help='bookman json file', default='') 
        parser.add_argument('-d', '--books_dir', help='directory with the books', default='')
        parser.add_argument('-k', '--api_key', help='GoogleBooks API key string', default='')
        return parser.parse_args(args)
    
    def lib_attrs_setter(self, key, value):
        """Set lib_attrs with value if value is not the empty string"""
        if value:
            self.lib_attrs[key] = value

    def load_env(self):
        """Load configuration attributes from environment"""
        get_env = lambda attr : os.environ[attr] if attr in os.environ else '' 
        for attribute in self.attributes:
            self.lib_attrs_setter(attribute, get_env(attribute.upper()))

    def load_ini(self, args):
        """Read config file specified in argument, return dictionary with
        its values"""
        config = configparser.ConfigParser()
        path = Path(args.config).expanduser().absolute()
        if not path.is_file():
            self.write_default_ini(path)
        config.read(path)
        c = config['bookman']
        for attr in self.attributes:
            self.lib_attrs_setter(attr, c[attr])

    def config_from_args(self, args):
        """Set the configuration options from the cli arguments"""
        self.lib_attrs_setter('api_key', args.api_key)
        self.lib_attrs_setter('books_dir', args.books_dir)
        self.lib_attrs_setter('books_json', args.books_json)
        
    def write_default_ini(self, path):
        """Write a copy of the default configuration file to path"""
        default = Path(__file__).absolute().parent / 'config.ini'
        with default.open() as f:
            txt = f.read()
        with path.open('w') as f:
            f.write(txt)
 

def main():
    Interface.do()

if __name__ == '__main__':
    main()
