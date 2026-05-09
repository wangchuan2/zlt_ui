import os
import yaml
from dotenv import load_dotenv

load_dotenv()


class ConfigReader:
    _config = None

    @classmethod
    def get_config(cls):
        if cls._config is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml"
            )
            with open(config_path, "r", encoding="utf-8") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get_base_url(cls):
        return cls.get_config()["base"]["url"]

    @classmethod
    def get_timeout(cls):
        return cls.get_config()["base"]["timeout"]

    @classmethod
    def is_headless(cls):
        return cls.get_config()["base"]["headless"]

    @classmethod
    def get_username(cls):
        return os.getenv("TEST_USERNAME", cls.get_config()["credentials"]["username"])

    @classmethod
    def get_password(cls):
        return os.getenv("TEST_PASSWORD", cls.get_config()["credentials"]["password"])
