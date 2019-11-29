from bookman.model import Lib
from bookman.api import GoogleBooksApi
import subprocess, configparser, argparse, sys, os
from pathlib import Path

class Commands:
    """
    Class for cli functions of bookman
    """

    choices = 'dump search add list open'.split()

    @classmethod
    def route(cls, lib, command):
        """Router that invokes the correct method"""

    @classmethod
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

    @classmethod
    def list(self, top_args):
        """Lists all books in the library"""
        parser = argparse.ArgumentParser(description=self.list.__doc__)
        parser.add_argument('-f', '--format', default='isbn')
        args = parser.parse_args(top_args)
        books = self.lib.books
        for book in books:
            print(getattr(book, args.format))

    @classmethod
    def add(self, top_args):
        """Receive a list of ISBN values, looks up the information about those books
        and add the books found to bookman."""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('isbns', nargs='+', help='space separated isbns, use a - in the first position to read from stdin')
        args = parser.parse_args(top_args)
        isbns = sys.stdin if args.isbns[0] == '-' else args.isbns
        self.lib.add_books(isbns)
        self.lib.save()


    @classmethod
    def open(self, top_args):
        """Searches for books and call xdg-open on matches"""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('pattern')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.pattern)
        paths = self.lib.get_paths(books)
        for path in paths:
            subprocess.Popen(['zathura', str(path)], start_new_session=True)

    @classmethod
    def dump(self, top_args):
        """Write the book identified by the given ISBN to stdout"""
        parser = argparse.ArgumentParser(description=self.add.__doc__)
        parser.add_argument('isbn')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.pattern)
        paths = self.lib.get_paths(books)
        with paths[0].open('rb') as f:
            sys.stdout.buffer.write(f.read())



class Interface:
    """
    Initial parser for bookman.
    Sequentially source the configuration variables, parses the top lvl args
    and routes the arguments to the appropriate command.
    
    """
    #Makes use of metaprogramming and properties to sequentially set configurating
    #attributes

    def __init__(self):
        self.attributes = 'books_json api_key books_dir'.split()
        self.lib_attrs = {attr : '' for attr in self.attributes}

    def do(self):
        """Parse command line arguments, initialize and load Lib, route
        command to Command class"""
        args = self.parse()
        self.load_ini(args)
        self.load_env(args)
        self.config_from_args(args)
        lib = Lib(api=GoogleBooksApi, **self.lib_arguments)
        lib.load()
        Command.route(lib, args)

    def parse(self, args=sys.argv):
        """Parser for the top level arguments."""
        args = args[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument('command', choices=Commands.choices)
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
            self.write_default_config(path)
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
    interface = Interface()
    interface.parse()

if __name__ == '__main__':
    main()
