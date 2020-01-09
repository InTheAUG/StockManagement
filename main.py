from get import alphavantage as alpha
from common import *
from utils import build
import os

if not build.checkforhomedirs():
    build.makehomedir()

stock = ["TSLA", "MSFT", "AAPL"]

alpha.getstocklist(stock, size='full')

df = alpha.build_df()


breakpoint()


