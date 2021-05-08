import subprocess, sys
from abc import ABC, abstractmethod
from pathlib import Path


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

    domain = None

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
        query = self.domain.clean_filename(query) if file else query
        books = self.domain.get_books_from_query(query)
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
        query = self.domain.clean_filename(filename) if not query else query
        books = self.domain.get_books_from_query(query)
        # I feel like this method adds too much custom logic
        result = prompt(list(map(str, books)))
        file = Path(filename)
        target = file.parent / (result + file.suffix)
        print(target)


def get_controllers():
    return  [value for value in globals().values() 
             if hasattr(value, "__mro__") and Controller in value.__mro__]
