import subprocess, sys
from abc import ABC, abstractmethod
from pathlib import Path

from .utils import pascal_to_kebab
from bookman import settings


def prompt(lines):
    # type: list(str) -> str
    """Receives a list of strings and pass to fzf for prompting"""
    line = "\n".join(lines)
    fzf_input = bytes(line, "utf-8")
    # This is a beauty. FZF uses stderr as the TUI fd, so passing
    # the bookman's stderr means I can spawn fzf, interact with it and 
    # get its result.
    result = subprocess.run("fzf", input=fzf_input, stdout=subprocess.PIPE, stderr=sys.stderr)
    return result.stdout.decode("utf-8").strip("\n")


class Controller(ABC):
    """
    ABC Controller class for Bookman's commands.
    Uses convention over configuration to add commands.
    
    Command name will be taken from class name (from PascalCase to kebab-case).
    Class' docstring will act as the commands help message.

    Note: `run` should have the same number of arguments and their name must
    match the args added to the parser
    """

    api_domain = None
    file_system_domain = None
    parser = None

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Runs the controller. Argument number and names must match
        the arguments added to the parser.
        """
        pass

    @abstractmethod
    def add_args(self, parser):
        """
        Add arguments to the command parser.
        Be nice and add proper help messages to args as well.
        """
        pass


class Fetch(Controller):
    """
    Queries Books API for a book and returns a bookman 
    formatted string for the book
    """

    def add_args(self, parser):
        parser.add_argument("query", 
                help="Query to use while searching book")

        parser.add_argument("-f", "--file", 
            help="Indicates whether the query is a filename.\
            Filenames are pre-processed to improve results",
            action="store_true", default=False, required=False)

    def run(self, query, file=False):
        query = self.file_system_domain.filename_from_path(file) if file else query
        books = self.api_domain.get_books_from_query(query)
        result = prompt(list(map(str, books)))
        print(result)


class Update(Controller):
    """
    Rename a book file to follow bookman's name format.
    Use filename as query, or a user specified query"
    """

    def add_args(self, parser):
        parser.add_argument("filename", 
                help="File which will be renamed")

        parser.add_argument("--query", "-q", required=False, default="",
            help="User defined string to use as query")


    def run(self, filename, query=""):
        query = self.file_system_domain.filename_from_path(filename) if not query else query
        books = self.api_domain.get_books_from_query(query)
        result = prompt(list(map(str, books)))
        # I feel like this method adds too much custom logic
        file = Path(filename)
        bookman_dir = self.file_system_domain.get_bookman_path()
        target = bookman_dir / (result + file.suffix)
        file.rename(target)


class Open(Controller):
    """
    Lists all books in bookman dir, prompts user using fzf and opens it
    """
    def add_args(self, parser):
        pass

    def run(self):
        bookman_dir = Path(settings.DIR).expanduser().resolve()
        result = subprocess.run(f"cd {bookman_dir} && find . | cut -c3- | fzf", shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
        relative_path = result.stdout.decode("utf-8").strip("\n")
        full_path = bookman_dir / relative_path
        subprocess.run(f"nohup xdg-open '{full_path}' > /dev/null", shell=True)


def get_controllers():
    def predicate(value):
         return isinstance(value, type) and Controller in value.__mro__ and not value is Controller

    return  {pascal_to_kebab(value.__name__): value()
             for value in globals().values() if predicate(value)}
