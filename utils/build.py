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
        key = f.readline().replace("\n", "")

    os.environ[ALPHAVANTAGE_KEY_VAR]= key

    return


def remove_env():
    del os.environ[ALPHAVANTAGE_KEY_VAR]
    return


