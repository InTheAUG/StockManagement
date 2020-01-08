import os
import pathlib
from common import PATHS, MODELS, STOCKFILES, SAVEPATH

ALPHAVANTAGE_KEY_PATH = pathlib.Path(__file__).parent.parent / "alphavantagekey"
KEY_VAR = "ALPHAVANTAGE_API_KEY"


def checkforhomedirs():
    for path in PATHS:
        if not os.path.exists(path):
            return False

    return True


def makehomedir():
    os.makedirs(MODELS)
    os.mkdir(STOCKFILES)


def initialize_env():
    with open(ALPHAVANTAGE_KEY_PATH, "r") as f:
        key = f.readline()
    os.putenv(KEY_VAR, key)


def remove_env():
    os.unsetenv(KEY_VAR)


