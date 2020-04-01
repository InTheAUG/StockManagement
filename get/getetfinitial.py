import sys
import requests 
import pandas as pd 
from time import sleep
from bs4 import BeautifulSoup


URL = "https://de.extraetf.com/etf-profile/"

def joinDictList(ls): 
    dc = {}
    for d in ls: 
        dc.update(d)
    return dc

def getHTTP(isin): 
    raw = requests.get(URL + isin)

    if raw.status_code == 200: 
        return BeautifulSoup(raw.text, features='lxml')    
    return False


def parsetitle(soup): 
    ls = str(soup.title).replace("<title>","").replace("</title>", "").split("|")

    return {'name': ls[0].strip(), 'wkn':ls[2].replace(" ", "").strip()}


def parseStrings(dc): 
    rp = {
        "Physisch": "sampling",
        "Synthetisch": "synthetic", 
        "Thesaurierend": "reinvesting", 
        "Ausschüttend": "distributing", 
    }

    for key, val in dc.items(): 
        if key == 'name': 
            continue
        val = val.strip().replace(" ","").replace("%", "").replace(",", ".").replace("Mio.", "000000",).replace("€", "")

        if val in rp: 
            val = rp[val]
        try: 
            val = float(val)
        except ValueError: 
            pass

        dc[key] = val
    
    return dc


def getSoupInfo(soup): 
    info = joinDictList([{x[1].text.strip(): x[0].text} for x in [list(y.find_all('span')) for y in [x for x in list(soup.find_all('div')) if x.get('class') != None] if 'mb-2' in y.get('class') and 'flex-1' in y.get('class')]])

    info = parseStrings(info)
    return {
        'td': info['TD'],
        'ter': info['TER'],
        'repr': info['Indexabbildung'],
        'positions': info['Anzahl Positionen'],
        'retstrategy': info['Ertragsverwendung'],
    }
    

     
def buildETFDict(isin):

    etfdict = { 
        'NAME': None,
        'ISIN': isin,  
        'TD': None,
        'TER': None,
        'WKN': None,
        'Replication': None,
        'Positions': None,
        'Retstrategy': None,
    }
    if http := getHTTP(isin):
        title = parsetitle(http)
        etfdict['NAME'] = title['name'] 
        etfdict['WKN'] = title['wkn']

        info = getSoupInfo(http)
        etfdict['TD'] = info['td']
        etfdict['TER'] = info['ter']
        etfdict['Replication'] = info['repr']
        etfdict['Positions'] = info['positions']
        etfdict['Retstrategy'] = info['retstrategy']

        return etfdict
    else: 
        return False


def error(isin): 
    print("Could not process {}".format(isin))

def etfDBfromList(isin_list): 
    """
    Read an etf_list in format["ISIN Industry_descriptor",...] 
    and build a pandas-DataFrame from the obtained information. 
    """
    fonds = []

    with open("etffile") as f: 
        lines = [x.replace("\n","") for x in f.readlines()]

    for line in lines: 
        split = line.split()
        isin = split[0]
        ind = split[1]

        if data := buildETFDict(isin): 
            data['Industry'] = ind
            fonds.append(data)
        else:
            error(isin)

    return pd.DataFrame(fonds)

def main(): 
    fonds = []

    with open("etffile") as f: 
        lines = [x.replace("\n","") for x in f.readlines()]

    df = etfDBfromList(lines)
    return df 

if __name__ == "__main__": 
    import code 

    df = main()
    code.interact(local=locals())

