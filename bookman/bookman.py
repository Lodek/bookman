from bookman.model import Lib
from bookman.api import GoogleBooksApi
import subprocess, configparser, argparse, sys
from pathlib import Path

class Interface:
    """
    Class for cli functions of bookman
    """
    def parse(self):
        #ignoring top parser flags for now
        top_args = self.top_parser()
        params = self.config_from_file(top_args.config)
        self.lib = Lib(api=GoogleBooksApi, **params)
        self.lib.load()
        func = getattr(self, top_args.command)
        func(top_args.args)
        
    def top_parser(self, args=sys.argv):
        """Top level parser for the command arguments of bookman"""
        args = args[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument('command', choices='search add list open'.split())
        parser.add_argument('args', nargs=argparse.REMAINDER)
        parser.add_argument('-c', '--config', default='~/.bookman.ini', help='bookman config file')
        parser.add_argument('-f', '--books_json', help='bookman json file') 
        parser.add_argument('-d', '--books_dir', help='directory with the books')
        parser.add_argument('-k', '--api_key', help='GoogleBooks API key string')
        return parser.parse_args(args)

    def config_from_file(self, path):
        """Read config file specified in argument, return dictionary with
        its values"""
        config = configparser.ConfigParser()
        config.read(Path(path).expanduser().absolute())
        return config['bookman']

    def search(self, top_args):
        """Search library for books"""
        parser = argparse.ArgumentParser(description=self.search.__doc__)
        parser.add_argument('pattern')
        parser.add_argument('-f', '--format', default='isbn')
        args = parser.parse_args(top_args)
        books = self.lib.search(args.pattern)
        for book in books:
            print(getattr(book, args.format))

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
        
def main():
    interface = Interface()
    interface.parse()

if __name__ == '__main__':
    main()
