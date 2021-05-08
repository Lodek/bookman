import sys
import subprocess

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


class Handler:

    def __init__(self, domain):
        self.domain = domain


    def get_formatted_name(self, query, file=False):
        """ """
        query = self.domain.clean_filename(query) if file else query
        books = self.domain.get_books_from_query(query)
        result = prompt(list(map(str, books)))
        print(result)

    def open(self):
        pass

