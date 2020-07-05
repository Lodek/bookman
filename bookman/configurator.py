"""
Module for handling the python configuration loading process.
"""
import importlib
import logging
import os

from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigDoesNotExist(RuntimeError):
    """
    Exception for when the specified configuration file does not exist.
    """
    def __init__(self, path):
        msg = f'Error: File {path} not found'
        super().__init__(self, msg)


class InvalidConfig(RuntimeError):
    """
    Exception for when the configuration doesn't pass the validation
    """
    def __init__(self, violations):
        msg = f'Error: Config did not pass validations. {violations}'
        super().__init__(self, msg)


class Configurator:
    """
    Class to handle configuration setup.
    Receive a path to a python config file, create file with minal setup if
    file doesn't exist, load module, override value from environments,
    override from cli arguments and store resulting property dict
    in self.config.
    
    validator is a function of type dict => (bool, [str]),
    where it returns true if it's valid and a list of violation strings which is printed.

    Assume env vars are prefixed with `env_prefix`

    Create default configuration structure if no configuration is given.

    Throw error if specified config doesn't exist, unless init is True
    """
    def __init__(self, config_path, default_config_path, override_properties, env_prefix,
                 default_config_body, init=False, validator=None):
        self.config_path = config_path
        self.default_config_path = default_config_path
        self.override_properties = override_properties
        self.env_prefix = env_prefix
        self.default_config_body = default_config_body
        self.init = init
        self.validator = validator 


    def get_config(self):
        """
        Method attemps to load the user specified configuration file, if it fails and init is
        false, raise ConfigDoesNotExist, else it initializes the configuration with the
        specified defaults. If user does not provide a configuration file, load the default 
        config and if default config does not exist, create it. After loading module,
        override configuration dictionary with values from environment by looking for
        environment variables whose names match the keys in the configuration dictionary 
        prepended with `env_prefix`. Finally, override loaded config with the values set in
        override_properties, if they existed beforehand. Return loaded configuration as a dict
        """
        if self.config_path:
            config_path = Path(self.config_path)
            is_default = False
        else:
            config_path = self.default_config_path
            is_default = True

        logger.info(f'Using config_path={config_path}')

        if not config_path.exists():
            if self.init or is_default:
                self.init_config(config_path)
            else:
                logger.error('Config not found')
                raise ConfigDoesNotExist(config_path)

        config = self.load_config_module(config_path)
        config = self.override_from_environment(config)
        config = self.override_from_dict(config, self.override_properties)
        logger.info('Value override finished')
        if self.validator:
            valid, violations = self.validator(config)
            if not valid:
                e = InvalidConfig(violations)
                logger.exception('Validation failed', e)
                raise e
        logger.info('Config loaded config={config}')
        return config


    def init_config(self, config_path):
        """Initialize configuration file"""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
           f.write(self.default_config_body)
        logging.info('Initialized config at {config_path}')


    def load_config_module(self, config_path):
        """Import the given file and return object with config properties"""
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        config = vars(config)
        config = {key: value for key, value in config.items() if key not in globals()}
        logger.debug(f'Config module loaded. config={config}')
        return config

    def override_from_environment(self, config):
        """Attempt to update `config` with values from environment.
        Look for environment variables whose names are the same as the keys in `config`
        prefixed by `self.env_prefix`."""
        items = dict(**config)
        for key in items:
            try:
                name = f'{self.env_prefix}{key}'
                value = os.environ[name]
                items[key] = value
                logger.debug(f'Config value override from env, {name}={value}')
            except KeyError:
                pass
        logger.debug(f'Environment override finished config={items}')
        return items

    def override_from_dict(self, config, properties):
        """Update config with items in properties, if they exist"""
        logger.debug(f'Merging config with values from prop={properties}')
        items = dict(**config)
        for key, value in properties.items():
            items[key] = value
        logger.debug(f'Config merge result {config}')
        return items
