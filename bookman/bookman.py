import logging
import sys
import argparse

from .services import GBooksService, api_factory
from .domains import Domain
from .controllers import *
from bookman import settings


handler_map = {
    "fetch": "",
    "update": "",
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

    controllers = get_controllers()
    for controller in controllers:
        subparsers.add_parser(controller.__name__,
                              help=controller.__doc__)
    return parser



def main():
    api = api_factory(settings.API_KEY)
    service = GBooksService(api)
    domain = Domain(service)
    Controller.domain = domain

    parser = build_parser()
    args = parser.parse_args()

    #handler_function = handler_map[args.__dict__.pop("subcommand_name")]

    #handler_function(handler, **args.__dict__)


if __name__ == '__main__':
    main()
