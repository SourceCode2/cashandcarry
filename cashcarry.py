import ccxt
import requests
import time
import os, subprocess
import csv
import json
import datetime
import time
import hmac
from requests import Request, Session
import pandas as pd
from requests.sessions import get_environ_proxies

def spread(futures, spot):
    price_futures = float(futures['ask'])
    price_spot = float(spot['bid'])
    gain = (price_futures/price_spot-1)*100
    
    return gain

def apr(gain, id):
    timecode = id[-4:]
    oggi = datetime.date.today()
    
    if timecode[0] == "0":
        mese = int(timecode[1])
    else:
        mese = int(timecode[0:2])

    giorno = int(timecode[2:4])

    if oggi.month > mese:
        anno = oggi.year + 1
    else:
        anno = oggi.year

    scadenza = datetime.date(anno,mese,giorno)
    
    differenza = scadenza-oggi

    return gain/differenza.days*365

def main(capitale):
    dataid = list()
    datagain = list()
    dataapr = list()
    totale = list()
    exchange = ccxt.ftx()

    markets = exchange.fetch_markets()
    market2 = markets
    
    for i in markets:

        if i['future'] == True:
            if "MOVE" not in i['id']:
                for x in market2:
                    if x['id'] == f"{i['base']}/USD":
                        gain = spread(i['info'], x['info'])-0.17
                        if gain > 2:
                            dataid.append(f"({i['id']})/({x['id']})")
                            totale.append((round(gain, 4), gain/100*capitale , round(apr(gain, i['id']),4), apr(gain, i['id'])/100*capitale))

    df = pd.DataFrame(totale, index=dataid, columns=("profitto alla scadenza %", "profitto alla scadenza €", "guadagno annualizzato %(APR)", "guadagno annualizzato €"))
    df.sort_values(by=['guadagno annualizzato %(APR)'], inplace=True, ascending=False)
    return df
    """
    #Get SOL/BTC market price
    sol_ticker = exchange.fetch_ticker('SOL/BTC')
    sol_btc = sol_ticker['last']
    btc_sol = 1/sol_btc

    # calculate the 0.000057btc worth of solana
    sol_needed = round(btc_sol*0.00006, 3)
    """

