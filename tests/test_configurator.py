from bookman.configurator import Configurator
from unittest.mock import MagicMock, Mock
from unittest import TestCase, main
from pathlib import Path
import os


test_dir = Path(__file__).expanduser().absolute().parent
assets = test_dir / 'assets'

class ConfiguratorTest(TestCase):

    def test_init_config_properly_creates_directories(self):
        pass
        
    def test_module_loading_returns_object_with_valid_properties(self):
        path = assets / 'valid-config.py'
        configurator = Configurator(path, {})
        config = configurator.config
        self.assertEquals(config.foo, 10)
        
    def test_override_from_environment_update_values(self):
        new_foo = '11'
        os.environ['foo'] = new_foo
        path = assets / 'valid-config.py'
        configurator = Configurator(path, {})
        config = configurator.config
        self.assertEquals(config.foo, new_foo)
        

    def test_override_from_cli_upate_values(self):
        args = {'foo': 11}
        path = assets / 'valid-config.py'
        configurator = Configurator(path, args)
        config = configurator.config
        self.assertEquals(config.foo, 11)


if __name__ == '__main__':
    main()
