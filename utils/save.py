from common import MODELS, STOCKFILES, SAVEPATH, FILEPATHS
from .build import makehomedir, checkforhomedirs
import pickle
import os


def save_to_pickle(model, filename):
    with open(MODELS + filename, "wb") as f:
        pickle.dump(model, f)
    return


def load_from_pickle(filepath):
    with open(filepath, "rb") as f:
        obj = pickle.load(f)

    return obj

