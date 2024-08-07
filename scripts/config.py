import configparser

def load_config(config_file='config/settings.cfg'):
    # Load config file
    config = configparser.ConfigParser()
    config.read(config_file)
    return config('DEFAULT')