import os
from importlib import import_module

settings = import_module(os.getenv("SETTINGS_MODULE", "dgt_tests.default_settings"))