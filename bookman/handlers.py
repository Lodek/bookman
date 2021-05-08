import subprocess

def prompt(lines):
    # type: list(str) -> str
    """Receives a list of strings and pass to fzf for prompting"""
    # well crap. I need to exec this. how do?
    fzf_input = "\n".join(str(lines))
    result = subprocess.run("fzf", input=fzf_input, capture_output=True, text=True)
    return result.stdout


class Handler:

    def __init__(self, domain):
        self.domain = domain


    def get_formatted_name(self, query, file=False):
        """ """
        query = self.domain.clean_filename(query) if file else query
        books = self.domain.get_books_from_query(query)
        for book in books:
            print(str(book))
