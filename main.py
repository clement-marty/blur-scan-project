import os
import configparser

from app import Application

basedir = os.path.dirname(__file__)

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.path.join(basedir, "config.ini"))
    return config


if __name__ == "__main__":
    config = load_config()
    app = Application(config, basedir)
    app.mainloop()