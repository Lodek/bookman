from pathlib import Path
bookman_config_dir = Path('~/.config/bookman').expanduser().absolute()
default_config_path = bookman_config_dir / 'config.py'
env_var_prefix = 'BOOKMAN_'
default_config_body = 'from bookman.config import *\n'
config_env_var_name = 'BOOKMAN_CONFIG'

