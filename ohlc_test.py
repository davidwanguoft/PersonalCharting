#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:28:19 2018

@author: dwang
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas
import datetime as dt
import numpy as np
import urllib
import os

from matplotlib import style
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies


ts = TimeSeries(key='ETQAVYR3G0OGHNRN',output_format='pandas',indexing_type='date')

# data decoder based on encoder: datestamps from AV api to matplotlib understandable format
def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

# master function
def graph_data(stock):
    data, meta_data = ts.get_daily(symbol=stock,outputsize='full')
    
    # date stripper
    data['date1'] = data.index
    z = 0
    metadate = []
    
    for z in range(len(data['date1'])):
        metadate.append(data['date1'][z])
    
    date = np.loadtxt(metadate, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y-%m-%d')})
    
    x = 0
    y = len(data['1. open'])
    ohlc = []
    
    while x < y:
        append_me = date[x], data['1. open'][x], data['2. high'][x], data['3. low'][x], data['4. close'][x], data['5. volume'][x]
        ohlc.append(append_me)
        x += 1
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))
    
    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879',colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(data)
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2,hspace=0)
    plt.show()

graph_data('MSFT')
