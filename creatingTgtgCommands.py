from tgtg import TgtgClient
import sys
import os
from datetime import datetime,timezone
import time
import tgtgClass
"""
FOR USE IN HOME TERMINAL
CODE WILL CREATE TOKENS.TXT FILE TO STORE CREDENTIALS
WILL TAKE USER INPUT TO EITHER 
1. ORDER FROM STORE
2. GET NOTIFCIATIONS FROM A STORE

"""
class tgtgCommands:

    def __init__(self, timezone=timezone.utc):
        self.timezone = timezone
        self.client = None


    #Token creation is done through users computer not AWS
    def startUp(self, emailToUse):
        if os.path.exists("commands.txt"):
            os.remove("commands.txt")
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
        reading.close()
        writing = open("commands.txt", "w")
        writing.write(f"access_token: {access_token}\n")
        writing.write(f"refresh_token: {refresh_token}\n")
        writing.write(f"cookie: {cookie}\n")
        writing.write("connection\n")
        writing.close()
        client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        return client


    def creatingNotfication(self):
        writing = open("commands.txt", "a")
        items = client.get_items()
        possibleOrders = {}
        currOrder = 1
        for item in items:
            item = client.get_item(item['item']['item_id'])
            possibleOrders[currOrder] = item
            print(f"Option {currOrder}: {item['store']['name_name']}")
            currOrder += 1
        print("_"*50)
        print("Type *all* to see all possible options or q to quit")
        while True:
            userChoice = input("Which option would you like to be notified about?")
            if userChoice.isdigit():
                if int(userChoice) not in possibleOrders:
                    print("Invalid option")
                    continue
                else:
                    print(f"Store choosen is {possibleOrders[int(userChoice)]['store']['store_name']}")
                    if input("To Confirm this store type y, to cancel type anything else") != 'y':
                        continue
                    print("Will notify you when the item is avaliable")
                    while True:
                        choice = input("Will check availability for how long in hours?")
                        if not choice.isdigit() or int(choice) < 0:
                            print("Invalid time")
                            continue
                        else:
                            duration = int(choice)
                            break
                    writing.write("item_id:" + possibleOrders[int(userChoice)]['item']['item_id'] + "\n")
                    writing.write("duration:" + str(duration) + "\n")
                    writing.write("type:notify\n")




    def orderAnItem(self, item):
        writing = open("commands.txt", "a")
        items = client.get_items()
        possibleOrders = {}
        currOrder = 1
        for item in items:
            item = client.get_item(item['item']['item_id'])
            if 'pickup_interval' not in item or 'next_sales_window_purchase_start' not in item:
                continue 
            print(item['store']['store_name'])
            startInt = datetime.strptime(item['pickup_interval']['start'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            endInt = datetime.strptime(item['pickup_interval']['end'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            salesWindow = datetime.strptime(item['next_sales_window_purchase_start'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            print(f"Option {currOrder}: At store {item['store']['store_name']} \n" +
                f"Start time: {startInt}, end time: {endInt} ")
            print(f"Next Sales window is at: {salesWindow}")
            possibleOrders[currOrder] = item
            currOrder += 1
        print("_"*50)
        print("Type *all* to see all possible options or q to quit")
        while True:
            order = (input("Which option would you like to order?"))

            if not order.isdigit() or (int(order) not in possibleOrders):
                if order.isdigit():
                    print("Invalid option")
                    continue
                elif order == "all":
                    for item in possibleOrders:
                        print(f"Option {item}: At store {possibleOrders[item]['store']['store_name']}")
                elif order == 'q':
                    break
                else:
                    print("Invalid option")
                    continue
            else:
                print(f"Ordering from store {order['store']['store_name']}")
                if input("To Confirm this store type y, to cancel type anything else") != 'y':
                    continue
                order = int(order)
                order = possibleOrders[order]
                print("How long would you like to attempt the order?")
                print("Duration will be after the next sales window")
                while (time := input("Duration in minutes: ")):
                    if not time.isdigit():
                        print("Invalid time")
                        continue
                    time = int(time)
                    if time < 0:
                        print("Invalid time")
                        continue
                    break
            break
        writing.wrote("item_id:" + order['item']['item_id'] + "\n")
        writing.write("duration:" + str(time) + "\n")
        writing.write("type:order\n")
        writing.close()
            
                



def creatingCommands():
    #this will create commands from the user to be executed possible command string
    """
    skip 
    order xyz 3 hours starting at 3:00 5 second intervals notfication system waitTime if confirmed

    """
    setUp = tgtgTesting()
    client = setUp.startUp(input("Enter your email or type skip of tokens.txt already contains keys: ")) 
    