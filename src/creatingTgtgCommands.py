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
        self.client = client
        return self.createClient()

    #creates the client
    def createClient(self):
        if not os.path.exists("tokens.txt"):
            if os.path.exists("src/tokens.txt"):
                reading = open("src/tokens.txt", "r")
            else:
                print("No tokens.txt file found")
                return
        else:
            reading = open("tokens.txt", "r")
        access_token = reading.readline().strip()
        refresh_token = reading.readline().strip()
        cookie = reading.readline().strip()
        reading.close()
        writing = open("commands.txt", "w")
        writing.write(f"channelID:{1338537091142778924}\n")
        writing.write(f"access_token:{access_token}\n")
        writing.write(f"refresh_token:{refresh_token}\n")
        writing.write(f"cookie:{cookie}\n")
        writing.write("type:connection\n")
        writing.close()
        self.client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        return self.client

    #notify if a store is avaliable has option to order
    def creatingNotfication(self, orderOrNot=False):
        writing = open("commands.txt", "a")
        items = self.client.get_favorites()
        possibleOrders = {}
        currOrder = 1
        for item in items:
            item = self.client.get_item(item['item']['item_id'])
            possibleOrders[currOrder] = item
            print(f"Option {currOrder}: {item['store']['store_name']}")
            currOrder += 1
        print("_"*50)
        print("Type *all* to see all possible options or q to quit\n" + 
            "Type each number seperated by a space to choose multiple options")
        while True:
            userChoice = input("Which options would you like to be notified about" + (" and ordered?" if orderOrNot else "?"))

            if userChoice == 'q':
                return
            elif userChoice == "all":
                for item in possibleOrders:
                    print(f"Option {item}: At store {possibleOrders[item]['store']['store_name']}")
                print("_"*50)
            elif userChoice.isdigit():
                if int(userChoice) not in possibleOrders:
                    print("Invalid option")
                    continue
                else:
                    print(f"Store choosen is {possibleOrders[int(userChoice)]['store']['store_name']}")
                    if input("To Confirm this store type y, to cancel type anything else:") != 'y':
                        continue
                    print("Will notify you when the item is avaliable")
                    while True:
                        choice = input("Will check availability for how long in hours?")
                        if not choice.isdigit() or int(choice) < 0:
                            print("Invalid time")
                            continue
                        else:
                            duration = int(choice)
                            writing.write("item_id:" + possibleOrders[int(userChoice)]['item']['item_id'] + "\n")
                            writing.write("duration:" + str(duration) + "\n")
                            writing.write("type:" + ("forceOrder" if orderOrNot else "notify") + "\n")
                            return
            else:
                parts = userChoice.strip().split(" ")
                for part in parts:
                    if not part.isdigit() or int(part) not in possibleOrders:
                        print("Invalid option")
                        continue
                print("stores choosen are: ")

                for part in parts:
                    print(f"{possibleOrders[int(part)]['store']['store_name']}")
                if input("To Confirm these stores type y, to cancel type anything else:") != 'y':
                    continue
                choice = input("Will check availability for how long in hours?")
                if not choice.isdigit() or int(choice) < 0:
                    print("Invalid time")
                    continue
                else:
                    duration = int(choice)
                    allParts = "item_id:"
                    for part in parts:
                        allParts += possibleOrders[int(part)]['item']['item_id'] + ","
                    allParts = allParts[:-1]
                    writing.write(allParts + "\n")
                    writing.write("duration:" + str(duration) + "\n")
                    writing.write("type:" + ("forceOrder" if orderOrNot else "notify") + "\n")
                    return


    def forceOrder(self):
        writing = open("commands.txt", "a")
        items = self.client.get_favorites()
        possibleOrders = {}
        currOrder = 1
        for item in items:
            item = self.client.get_item(item['item']['item_id'])
            possibleOrders[currOrder] = item
            print(f"Option {currOrder}: {item['store']['store_name']}")
            currOrder += 1
        print("_"*50)
        print("Type *all* to see all possible options or q to quit")
        while True:
            userChoice = input("Which option would you like to be order?")
            if userChoice == 'q':
                return
            elif userChoice == "all":
                for item in possibleOrders:
                    print(f"Option {item}: At store {possibleOrders[item]['store']['store_name']}")
                print("_"*50)
            elif userChoice.isdigit():
                if int(userChoice) not in possibleOrders:
                    print("Invalid option")
                    continue
                else:
                    print(f"Store choosen is {possibleOrders[int(userChoice)]['store']['store_name']}")
                    if input("To Confirm this store type y, to cancel type anything else:") != 'y':
                        continue
                    print("Will notify you when the item is avaliable")
                    while True:
                        choice = input("Will check availability for how long in hours?")
                        if not choice.isdigit() or int(choice) < 0:
                            print("Invalid time")
                            continue
                        else:
                            duration = int(choice)
                            writing.write("item_id:" + possibleOrders[int(userChoice)]['item']['item_id'] + "\n")
                            writing.write("duration:" + str(duration) + "\n")
                            writing.write("type:notify\n")
                            return




    #order an item with a pickup window and next sale interval
    def orderAnItem(self):
        writing = open("commands.txt", "a")
        items = self.client.get_favorites()
        possibleOrders = {}
        currOrder = 1
        for item in items:
            item = self.client.get_item(item['item']['item_id'])
            if 'pickup_interval' not in item or 'next_sales_window_purchase_start' not in item:
                continue 
            startInt = datetime.strptime(item['pickup_interval']['start'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            endInt = datetime.strptime(item['pickup_interval']['end'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            salesWindow = datetime.strptime(item['next_sales_window_purchase_start'], "%Y-%m-%dT%H:%M:%SZ").astimezone(self.timezone)
            print(f"Option {currOrder} at store: {item['store']['store_name']} \n" +
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
                    for position in possibleOrders:
                        print(f"Option {position}: At store {possibleOrders[position]['store']['store_name']}")
                    print("_"*50)

                elif order == 'q':
                    return
                else:
                    print("Invalid option")
                    continue
            else:
                order = int(order)
                order = possibleOrders[order]
                print(f"Ordering from store {order['store']['store_name']}")
                if input("To Confirm this store type y, to cancel type anything else") != 'y':
                    continue
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
        writing.write("item_id:" + order['item']['item_id'] + "\n")
        writing.write("duration:" + str(time) + "\n")
        writing.write("type:order\n")
        writing.close()
            
                



def creatingCommands(notification=False, order=False, forceOrder=False):
    #this will create commands from the user to be executed possible command string
    """
    skip 
    order xyz 3 hours starting at 3:00 5 second intervals notfication system waitTime if confirmed

    """
    setUp = tgtgCommands()
    client = setUp.startUp(input("Enter your email or type skip of tokens.txt already contains keys: ")) 

    if order:
        setUp.orderAnItem()
    if notification:
        setUp.creatingNotfication()
    if forceOrder:
        setUp.forceOrder()


if __name__ == "__main__":
    creatingCommands(notification=True)

    