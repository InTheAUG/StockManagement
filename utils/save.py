from ..classes.stockclass import Stock

def save(stock):
   pass

def load(symbol):
    with open(symbol+'.save', 'r') as f:
        data = [x.strip('\n') for x in f.readlines()]

    stock = Stock()

    return stock
