# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 19:33:32 2018

@author: Jan.Fait
"""

import googlemaps
import pandas
import datetime
from .  import prgcollector
import os

#initialize client
API_KEY = os.getenv("KEY")
gm = googlemaps.Client(key=API_KEY)

#load street data
streets = pandas.read_csv("C:/Users/jan.fait/Documents/Data/prague_7_streets.csv",sep=";")
#filter out some rogue p6 streets
streetsP7 = streets.loc[streets['district_code']=='Praha 7']
#create a column for geocodings
streetsP7 = streetsP7.assing(full=pandas.Series(streetsP7['street']+" , "+streetsP7['district_code']).values)

#initialize the instance of PrgCollector
prg = PrgCollector(gmClient = gm,debug=True)
#collect the geocodes
geocodes = prg.geoCode(list(streetsP7['full']))
#assign into the existing data frame
streetsP7 = streetsP7.assign(lat=pandas.Series([x[0] for x in geocodes]).values)
streetsP7 = streetsP7.assign(lon=pandas.Series([x[1] for x in geocodes]).values)




