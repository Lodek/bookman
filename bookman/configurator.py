import importlib, os

class Configurator:
    """
    Class to handle configuration setup.
    Receive a path to a python config file, create file with minal setup if 
    file doesn't exist, load module, override value from environments,
    override from cli arguments and store resulting property dict
    in self.config.
    """
    def __init__(self, path, properties):
        self.config = None
        self.path = path
        self.init_config_if_missing()
        self.load_config()
        self.override_from_environment()
        self.override_from_cli(properties)

    def init_config_if_missing(self):
        """Write minimal config if missing"""
        txt = 'from bookman.config import *\n'
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open('w') as f:
                f.write(txt)

    def load_config(self):
        """Import the given file and return object with config properties"""
        spec = importlib.util.spec_from_file_location("config", self.path)
        self.config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.config)

    def override_from_environment(self):
        """Override config values from environment variables, if they exist"""
        items = vars(self.config)
        for key in items:
            try:
                items[key] = os.environ[key]
            except KeyError:
                pass
        
    def override_from_cli(self, properties):
        """Override config values from cli arguments"""
        items = vars(self.config)
        for key, value in properties.items():
            items[key] = value
 
