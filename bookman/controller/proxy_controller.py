"""
Initial parser for bookman.
Sequentially source the configuration variables, parses the top lvl args
and routes the arguments to the appropriate command.
"""
import argparse, os, re
from pathlib import Path
from bookman.api_wrapper import ApiWrapper
from bookman.model import Lib, Book
import bookman.properties as props
from bookman.configurator import Configurator

import bookman.controller.commands as commands
from bookman.controller.abc import ControllerABC

class ProxyController(ControllerABC):

    def __init__(self):
        controllers = list(commands.get_commands(vars(commands)))
        self.choices = [controller.command_name for controller in controllers]
        self.command_lookup = {controller.command_name: controller for controller in controllers}
        super().__init__()
        
    def command_name(self):
        return 'bookman'

    @staticmethod
    def validator(config):
        if not config['api_key'] or not config['api_key_file']:
            return (False, ['Must specify either api key or api key file'])
        else:
            return (True, [])

    def _controller(self, args):
        """Parse command line arguments, initialize and load Lib, route
        command to Command class"""
        try:
            config_path = os.environ[props.config_env_var_name]
        except KeyError:
            config_path = ''
        config_path = args.config if args.config else config_path
        cli_properties = self._parse_cli_properties(args.p)
        configurator = Configurator(config_path, props.default_config_path, cli_properties,
                                    props.env_var_prefix, props.default_config_body,
                                    validator=self.validator)
        config = configurator.get_config()
        if config['api_key_file']:
            try:
                with open(config['api_key_file']) as f:
                    key = f.read().strip('\n')
                    config['api_key'] = key
            except FileNotFoundError:
                exit(f"Error: Cant find api file {config['api_key_file']}")
        wrapper = ApiWrapper(config)
        Book.inject_attributes(config['extra_attrs'])
        lib = Lib(api=wrapper, books_json=config['books_json'], books_dir=config['books_dir'])
        lib.load()
        self._proxy(lib, args.command, args.args)

    def _proxy(self, lib, command, args):
        """Routes chosen command to one of the other controllers"""
        try:
            cls = self.command_lookup[command]
            cls.configure(lib)
            cls.run(args)
        except KeyError:
            raise RuntimeError((f'{command} is not a valid command.'))

    def _parse_cli_properties(self, property_list):
        validator = re.compile(r'(\d|\w|_)+?=(.*)')
        matches = [(p, validator.search(p)) for p in property_list]
        violations = filter(lambda match: not match[1], matches)
        error_msgs = [f'Property {violation} is invalid, must follow var=value.'
                      for violation in violations]
        if error_msgs:
            raise RuntimeError('\n'.join(error_msgs))
        return {match.group(1): match.group(2) for _, match in matches}


    def parser_config(self):
        self.parser.add_argument('command', choices=self.choices)
        self.parser.add_argument('args', nargs=argparse.REMAINDER)
        self.parser.add_argument('-c', '--config', required=False, default='',
                                 help='bookman config file')
        self.parser.add_argument('-p', required=False, default=[], action='append',
                                 help='Sets a property in the format key=value. Will override value in user defined config')

