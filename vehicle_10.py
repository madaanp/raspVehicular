from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket
from datetime import datetime, timedelta
import json

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

accidentDataPostResponse = None

def storeAccidentData(message):
    accidentDataFetched = []
    if "body" in message:
        print("hola",message)
        output = message['body']
        print(output)
        for acccidentSignal in output:
            timestamp = acccidentSignal['timeStamp']
            date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if abs(datetime.now() - date_time_obj) < timedelta(minutes=500):
                accidentDataFetched.append(acccidentSignal)
            print("******")
        return accidentDataFetched
    else:
        return accidentDataFetched

def my_publish_callback(envelope, status):
   # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        if message.message == None:
            continue_moving()
        else:
            print("From RSU-5 : ",message.message)
            continue_moving(message.message)

#RSU 5
RSU_coords = [53.377350, -6.248184]
vehicle_10_start_coords = [53.378550, -6.247462]
vehicle_10_stop_coords = [53.372867, -6.239719]
junction_coords = [53.375804, -6.250268]

def continue_moving(message):
    accidentDataFetched = storeAccidentData(message)
    print(accidentDataFetched)
    pubnub.unsubscribe().channels("RSU-5").execute()
    if(len(accidentDataFetched) > 0):
        getToAccidentLocation(accidentDataFetched)
    else:
        print("No accidents detected ! ")

def getToAccidentLocation(accidentDataFetched):
    pubnub.unsubscribe().channels("RSU-5").execute()
    accidentCount = len(accidentDataFetched)
    print(accidentCount, "accidents detected ! ")
    vehicle_lane_change_coords = []
    arrayCounter = 0
    accident_coords = []
    for accidentLoc in accidentDataFetched:
        vehicle_lane_change_coords.append([accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']])
        accident_coords.append([accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']])
    print(vehicle_10_start_coords)
    print(vehicle_10_stop_coords)
    print("Junction loc - ", junction_coords)
    
    # 53.37735 -6.248182
    while((geodesic(vehicle_10_start_coords,junction_coords).m) > 15):
        print("Distance to Junction (metres): ",geodesic(vehicle_10_start_coords,junction_coords).m)
        # time.sleep(0.2)
        vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] - 0.0000049),6)
        vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] + 0.0000464),6)
        print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1])
    print("Vehicle at junction..")
    print("Changing lanes to avoid traffic congestion..")
    
    # Change vehicle_10_stop_coords to accident coords - accident_coords
    while(vehicle_10_start_coords[0] <= vehicle_10_stop_coords[0] and vehicle_10_start_coords[1] <= vehicle_10_stop_coords[1]):
            vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] + 0.0005),6)
            vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] + 0.0005),6)
            print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1])
    print("Ambulance reached the accident location !")

def moving_vehicle():
    while((geodesic(vehicle_10_start_coords,RSU_coords).m) > 15):
        print("Distance to RSU-5 (metres): ",geodesic(vehicle_10_start_coords,RSU_coords).m)
        time.sleep(0.5)
        vehicle_10_start_coords[0] = round((vehicle_10_start_coords[0] - 0.0002400),6)
        vehicle_10_start_coords[1] = round((vehicle_10_start_coords[1] - 0.0001444),6)
        print("Current Coordinates", vehicle_10_start_coords[0],vehicle_10_start_coords[1])
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("RSU-5").execute()
moving_vehicle()