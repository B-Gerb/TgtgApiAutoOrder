from tgtg import TgtgClient
import sys
import os
from datetime import datetime
import time
import tgtgClass
"""
FOR USE IN HOME TERMINAL
CODE WILL CREATE TOKENS.TXT FILE TO STORE CREDENTIALS
WILL TAKE USER INPUT TO EITHER 
1. ORDER FROM STORE
2. GET NOTIFCIATIONS FROM A STORE

"""
class tgtgTesting:

    def __init__(self):
        self.client = None

    def startUp(self, emailToUse):
        if emailToUse == "skip":
            return self.createClient()
        client = TgtgClient(email=emailToUse)
        credentials = client.get_credentials()
        if os.path.exists("tokens.txt"):
            os.remove("tokens.txt")
        
        writing = open("tokens.txt", "w")
        writing.write(credentials['access_token'] + "\n")
        writing.write(credentials['refresh_token'] + "\n")
        writing.write(credentials['cookie'] + "\n")
        writing.close()
        return self.createClient()

    def createClient(self):
        reading = open("tokens.txt", "r")
        access_token = reading.readline().strip()
        refresh_token = reading.readline().strip()
        cookie = reading.readline().strip()
        client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        return client


    def orderAnItem(self, item):
        print(f"Attempting to order from store {item['store']['store_name']}")
        print("Starting ordering process")
        failing = True
        while failing:
            try:    
                order = self.client.create_order(item['item']['item_id'], 1)
                print(order)
                print("order created")
                failing = False
                return order
            except:
                print("Failed to order")
            time.sleep(3)
        print(order)


    def createNotification(self, item):
        print(f"Attempting to order from store {item['store']['store_name']}")
        print("Starting ordering process")
        failing = True
        while failing:
            try:    
                order = self.client.create_order(item['item']['item_id'], 1)
                print(order)
                print("order created")
                failing = False
                return order
            except:
                print("Failed to order")
            time.sleep(3)
        print(order)