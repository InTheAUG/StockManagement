from get import alphavantage as alpha
import common
from utils import build

build.mkhomedirs(common.FILEPATHS)

stock = ["IXIC"]

alpha.getstocklist(stock)

df = alpha.build_df()

breakpoint()


