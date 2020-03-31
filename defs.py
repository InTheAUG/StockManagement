from pathlib import Path
import os

ALPHAVANTAGE_KEY_PATH = Path(__file__).parent/ "alphavantagekey"

SAVEPATH = "/home/" + os.getenv('USERNAME') + "/.stock/"

MODELS = SAVEPATH + "models/"
STOCKFILES = SAVEPATH + "stockfiles/"
FILEPATHS = [SAVEPATH, MODELS, STOCKFILES]

ALPHAVANTAGE_KEY_VAR = "ALPHAVANTAGE_API_KEY"
