from abc import ABC, abstractmethod
from argparse import ArgumentParser

class ControllerABC(ABC):
    """
    Abstract base class for a bookman command.
    Has method to add arguments to parser.
    Define a common interface for all commands to be called.
    Override docstring to add documentation about command in CLI.
    Override command_name to define the CLI keyword to invoke this command.
    """
    def __init__(self):
        self.lib = None
        self.parser = ArgumentParser(description=self.__doc__)
        self.parser_config()

    def configure(self, lib):
        self.lib = lib
    
    @property
    @abstractmethod
    def command_name(self):
        """Property that maps the cli argument which triggers this command"""
        pass

    @abstractmethod
    def parser_config(self):
        """Add arguments for the current command"""
        pass

    @abstractmethod
    def _controller(self, args):
        """Defines the controller method for the command class."""
        pass

    def run(self, args):
        """Interface to call a command, receive arguments to be processed by args """
        parsed = self.parser.parse_args(args)
        self._controller(parsed)
        
    @classmethod
    def command_factory(cls, config):
        pass
