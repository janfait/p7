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