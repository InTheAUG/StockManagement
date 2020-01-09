import os
import pathlib
from common import FILEPATHS, MODELS, STOCKFILES, SAVEPATH, ALPHAVANTAGE_KEY_PATH, ALPHAVANTAGE_KEY_VAR


def checkforhomedirs():
    for path in FILEPATHS:
        if not os.path.exists(path):
            return False

    return True


def makehomedir():
    os.makedirs(MODELS)
    os.mkdir(STOCKFILES)


def initialize_env():
    with open(ALPHAVANTAGE_KEY_PATH, "r") as f:
        key = f.readline()
    os.putenv(ALPHAVANTAGE_KEY_VAR, key)


def remove_env():
    os.unsetenv(ALPHAVANTAGE_KEY_VAR)


