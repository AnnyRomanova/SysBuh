import logging.config
import yaml
import os

def setup_logging():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "logging.yaml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    config['handlers']['file']['filename'] = os.path.join(log_dir, "app.log")

    logging.config.dictConfig(config)
