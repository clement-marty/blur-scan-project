import configparser
import tkinter as tk

from app import Application


def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


if __name__ == "__main__":
    config = load_config()
    app = Application(config)
    app.mainloop()