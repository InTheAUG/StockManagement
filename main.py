from get import alphavantage as alpha
from common import *
from utils import build
import os

if not build.checkforhomedirs():
    build.makehomedir()

stock = ["TSLA", "MSFT", "AAPL"]

df = alpha.build_df()

breakpoint()


