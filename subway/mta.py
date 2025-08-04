import time
import time
import time
import time
import time

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
import requests
import datetime
import time
import sys
from datetime import datetime

apikey = "pr2M7OgOQb9R8cJs5109c8yoUjzMIirk4L0YuxtT"

BDFMfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm' # B,D,F,M
ACEHfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace' # A,C,E,H 
Lfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l' # L 
JZfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz' # JZ 

class Train:
    def __init__(self, name="", time=""):
        self.name = name
        self.time= time

def getB26():
    response_bus = requests.get("http://gtfsrt.prod.obanyc.com/tripUpdates?key=b871cb82-6ba0-4a11-985c-d732573c9dba")
    feed_bus = gtfs_realtime_pb2.FeedMessage()
    feed_bus.ParseFromString(response_bus.content)
    bus_feed = protobuf_to_dict(feed_bus)
    realtime_bus = bus_feed['entity']

    busTrips = []
    for bus in realtime_bus:
        if bus.get('trip_update'):
            if (bus['trip_update'].get('stop_time_update')):
                # get for each stop time update that is at our stop
                for update in bus['trip_update'].get('stop_time_update'):
                    stop_id = update['stop_id']
                    if (stop_id == "302499"):
                        elapsed = update['arrival']['time']-time.mktime(datetime.now().timetuple())

                        mins = int(elapsed / 60)
                        secs = int(elapsed % 60)

                        # Round to nearest minute
                        if (secs > 30):
                            mins = mins + 1

                        # Skips less than 4
                        if (mins < 4):
                            continue
                        busTrips.append(Train("B26", mins))
    return busTrips



def gettimes(jzFeed, cFeed, JS, CN):
    global apikey
    
    # Request parameters
    headers = {'x-api-key': apikey}
    
    # Get the train data from the MTA
    response_jz = requests.get(jzFeed, headers=headers, timeout=30)
    

    # Parse the protocol buffer that is returned
    feed_jz = gtfs_realtime_pb2.FeedMessage()
    feed_jz.ParseFromString(response_jz.content)

    response_c = requests.get(cFeed, headers=headers, timeout=30)
    feed_c = gtfs_realtime_pb2.FeedMessage()
    feed_c.ParseFromString(response_c.content)

    # Get a list of all the train data
    subway_feed_jz = protobuf_to_dict(feed_jz) # subway_feed is a dictionary
    subway_feed_c = protobuf_to_dict(feed_c)
    realtime_jz = subway_feed_jz['entity']
    realtime_c = subway_feed_c['entity']
    

    subway_feed = subway_feed_jz.update(subway_feed_c)
    
    realtime_data = realtime_jz+realtime_c

    trainTrips = []

    for train in realtime_data:
        if train.get('trip_update'):
            if (train['trip_update'].get('stop_time_update')):
                for update in train['trip_update'].get('stop_time_update'):
                    stop_id = update['stop_id']

                    if (stop_id in [JS]):

                        # Get the number of seconds from now to the arrival time
                        elapsed = update['arrival']['time']-time.mktime(datetime.now().timetuple())
                        
                        route_id = (train['trip_update']['trip']['route_id'])[0]
                        #Ignore Z trains
                        if (route_id == "Z"):
                            continue
                        # Calculate minutes and seconds until arrival
                        mins = int(elapsed / 60)
                        secs = int(elapsed % 60)

                        # Round to nearest minute
                        if (secs > 30):
                            mins = mins + 1

                        # Skips less than 9
                        if (mins < 9):
                            continue
                        
                        trainTrips.append(Train(route_id + "S", mins))
                    if (stop_id in [CN]):
                        # Get the number of seconds from now to the arrival time
                        elapsed = update['arrival']['time']-time.mktime(datetime.now().timetuple())

                        # If less than 10 minutes, skip it
                        if (elapsed < 10):
                            continue
                        
                        route_id = (train['trip_update']['trip']['route_id'])[0]

                        # Calculate minutes and seconds until arrival
                        mins = int(elapsed / 60)
                        secs = int(elapsed % 60)

                        # Round to nearest minute
                        if (secs > 30):
                            mins = mins + 1

                        # Skips less than 10
                        if (mins < 10):
                            continue
                        
                        trainTrips.append(Train("CN", mins))
                        
    
    return trainTrips

def getTrainTimes(JN, CN):
    global ACEHfeed
    global JZfeed

    lines = {"JS":[], "CN":[], "B26":[]}
    
    trainTripResults = gettimes(JZfeed, ACEHfeed, JN, CN)
    busTripResults = getB26()

    for train in trainTripResults:
            lines[train.name].append(train.time)

    for bus in busTripResults:
        lines[bus.name].append(bus.time) 

    for line in lines.keys():
        rawTimes = lines[line]
        lines[line] = sorted(set(rawTimes))[:3]
         
    return lines
                    

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print(getTrainTimes("M11S","A49N"))
    else:
        print(getTrainTimes(sys.argv[1],sys.argv[2]))
