from pathlib import Path
bookman_config = Path('~/.config/bookman').home().absolute()
default_config = bookman_config / 'config.py'
config_env_var_name = 'BOOKMAN_CONFIG'

