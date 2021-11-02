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

def spread(futures, spot):

    price_futures = float(futures['ask'])
    price_spot = float(spot['bid'])
    gain = (price_futures/price_spot-1)*100
    
    return gain


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
                        gain = spread(i['info'], x['info'])
                        if gain > 2:
                            if "1231" in i['id']:
                                dataid.append(f"({i['id']})/({x['id']})")
                                totale.append((round(gain, 2), gain/100*capitale ,round(gain/61*365, 2), gain/61*365/100*capitale))

                            elif "0325" in i['id']:
                                dataid.append(f"({i['id']})/({x['id']})")
                                totale.append((round(gain, 2), gain/100*capitale ,round(gain/61*365, 2), gain/174*365/100*capitale))

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

