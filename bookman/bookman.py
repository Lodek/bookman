import logging
import sys
import argparse

from .handlers import Handler
from .services import GBooksService, api_factory
from .domains import Domain
from bookman import settings


handler_map = {
    "fetch": Handler.get_formatted_name,
    "update": Handler.update_filename,
}


def setup_logging():
    logfmt = '%(asctime)s %(name)s %(funcName)s %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logfmt,
                        filename='bookman.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logfmt)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def build_parser():
    parser = argparse.ArgumentParser("Bookman")
    subparsers = parser.add_subparsers(dest="subcommand_name", required=True)

    filename_command = subparsers.add_parser("fetch", help="Queries API for a book and returns a bookman formatted string for the book")
    filename_command.add_argument("query", help="Query to use while searching book")
    filename_command.add_argument("-f", "--file", help="Indicates whether the query is a filename. Filenames are pre-processed to improve results",
            action="store_true", default=False, required=False)

    update_filename = subparsers.add_parser("update", 
            help="Rename a book file to follow bookman's name format. Use filename as query, or a user specified query")
    update_filename.add_argument("filename", help="File which will be renamed")
    update_filename.add_argument("--query", "-q", required=False, default="",
            help="User defined string to use as query")

    return parser



def main():
    api = api_factory(settings.API_KEY)
    service = GBooksService(api)
    domain = Domain(service)
    handler = Handler(domain)

    parser = build_parser()
    args = parser.parse_args()

    handler_function = handler_map[args.__dict__.pop("subcommand_name")]

    handler_function(handler, **args.__dict__)


if __name__ == '__main__':
    main()
