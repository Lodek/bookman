import logging
import sys
import argparse

from .services import GBooksService
from .domains import ApiDomain, FileSystemDomain, Parser
from .controllers import get_controllers, Controller
from bookman import settings


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

def build_parser(controller_map):
    parser = argparse.ArgumentParser("Bookman")
    subparsers = parser.add_subparsers(dest="subcommand_name",
                                       required=True)
    for command, controller in controller_map.items():
        subparser = subparsers.add_parser(command, help=controller.__doc__)
        controller.add_args(subparser)
    return parser

def main():
    controller_map = get_controllers()
    arg_parser = build_parser(controller_map)
    args = arg_parser.parse_args()

    service = GBooksService()
    api_domain = ApiDomain(service)
    filesystem_domain = FileSystemDomain()
    parser = Parser()
    Controller.api_domain = api_domain
    Controller.file_system_domain = filesystem_domain
    Controller.parser = parser

    command_name = args.__dict__.pop("subcommand_name")
    controller = controller_map[command_name]
    controller.run(**args.__dict__)


if __name__ == '__main__':
    main()
