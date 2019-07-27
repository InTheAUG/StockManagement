from classes import stockclass
import time

ls = ["TSLA", "ABT", "NSRGY"]
stock = []

for _ in ls:
    time.sleep(5)
    stock.append(stockclass.Stock(_, 100, 10, "NASDAQ", "2019-07-10"))

import code
code.interact(local=locals())
