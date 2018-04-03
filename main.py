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

#define collector class
class PrgCollector():
    
    gm = None
    types = []
    
    def __init__(self,gmClient = None,debug=False):
        self.gm = gmClient
        self.debug = debug
    
    def dprint(self,*args):
        """ Prints progress to console if class initialized with debug=True"""
        if self.debug:
           args = [str(x) for x in args]      
           out = " ".join(args)
           out = "PrgCollector at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': ' + out 
           print(out)
    
    def geoCode(self,address=None):
        data = []
        for a in  address:
            response = self.gm.geocode(a)
            data.append(list(response[0]['geometry']['location'].values()))
        return data
        
    def parseAddress(self,formatted_address,separator=","):
        asplit = formatted_address.split(separator)
        asplit = [x.strip() for x in asplit]
        street = asplit[0]
        district = asplit[1]
        street,streetn = street.rsplit(' ', 1)
        postcode = district[0:6].replace(" ", "")
        district = district[6:].strip()
        return [street,streetn,district,postcode]
    
    def getPlaces(self,query=None,location=[],radius=5000,collect=['place_id','name','formatted_address','rating','types']):
        token = None
        data = []
        response = self.gm.places(query=query,location=location,radius=radius)
        self.dprint("First response status: ",response["status"])
        while True:
            for p in response['results']:
                place = [p[x] for x in collect]
                data.append(place)
                #types.append(place['types'])
            if 'next_page_token' in response.keys():
                token = response['next_page_token']
                try:
                    response = self.gm.places(query=query,page_token=token)
                    break
                except:
                    pass
            else:
                break
        return data

#initialize the instance of PrgCollector
prg = PrgCollector(gmClient = gm,debug=True)
#collect the geocodes
geocodes = prg.geoCode(list(streetsP7['full']))
#assign into the existing data frame
streetsP7 = streetsP7.assign(lat=pandas.Series([x[0] for x in geocodes]).values)
streetsP7 = streetsP7.assign(lon=pandas.Series([x[1] for x in geocodes]).values)




