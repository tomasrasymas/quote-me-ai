from config import get_config


class ConfigMixin:
    @property
    def config(self):
        return get_config()