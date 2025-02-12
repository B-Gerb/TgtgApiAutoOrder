from tgtg import TgtgClient
import sys
import os
from datetime import datetime,timezone
import time


#Class for commands to go through tgtg
#This file will go AWS along with tokens.txt
#this is the script that will run, commands.txt will be the commands
class tgtgTesting:
    #intalize

    def __init__(self):
        self.client = None

    #creates the client
    def createClient(access_token, refresh_token, cookie):
        client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        notifyUser("connection", message= "Connection established")


    """
    Returns the order object if successful, otherwise returns "Failed to order"
    item: the item object
    duration: the time in minutes you want to wait to order the item after the next sales window
    """
    def orderAnItem(self, item, duration):
        time = item['next_sales_window_purchase_start']
        target_date = datetime.fromisoformat("time").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        time_to_wait = (target_date - now).total_seconds()
        time_to_wait = startTime - datetime.now(timezone.utc)
        time.sleep(time_to_wait.total_seconds()-3)
        duration +=3
        firstSpeed = 600
        while firstSpeed > 0:
            order = attemptToOrder(item['item']['item_id'], amt)
            if order != "Failed to order":
                notifyUser("order", order, message= "successful order")
                return
            else:
                time.sleep(1)
                firstSpeed -= 1
        secondSpeed = (duration*60) - 600
        while secondSpeed > 0:
            order = attemptToOrder(item['item']['item_id'], amt)
            if order != "Failed to order":
                notifyUser("order", order, message= "successful order")
                return
            else:
                time.sleep(10)
                secondSpeed -= 1
        notifyUser("order", message= "Failed to order")


    #force order an item even if it does not have any avaliable pickup window
    def forceOrder(self, item_id, duration):
        time = duration*3600
        while time > 0:
            order = self.client.create_order(item_id, amt)
            if order != "Failed to order":
                notifyUser("forceorder", order, message= "Force order placed")
                return
            else:
                time.sleep(10)
                time -= 10
         


    """
    item_id: the id of the item you want to be notified about
    duration: the time in minutes you want to be notified for in minutes
    """
    def checkAvaliable(self, item_id):
        item = client.get_item(item_id)
        if item['items_available'] > 0:
            return True
        else:
            return False
    
    def attemptToOrder(self, item_id, amt):
        try:
            order = self.client.create_order(item_id, amt)
            return order
        except:
            return "Failed to order"

    def notifyWhenAvaliable(self, item_id, duration):
        duration = duration*3600

        while duration > 0:
            item = client.get_item(item_id)
            if item['items_available'] > 0:
                notifyUser("notify", item, "Item is avaliable")
                return 
            time.sleep(10)
            duration -= 10
        notifyUser("notify", message= "Never became avaliable")
        
             



    """
    type: the type of notification, either order or notify
    """
    def notifyUser(self, type, item=None, message = None):
        if type == "order":
            print('place holder for order')
        elif type == "notify":
            print('place holder for avaiable')
        elif type == "forceorder":
            print('place holder for force order')
        elif type == "connection":
            print('place holder for connection')
        elif type == "abort":
            print('place holder for abort')
        else:
            return "Invalid type"

    def abortOrder(self, order_id):
        time.sleep(3)
        client.abort_order(order_id)
        notifyUser("abort", message= "Order aborted")

#If you want to start the client with a new email, use the startUp function
"""
Commandline starts with
access_token: tokenhere
refresh_token: tokenhere
cookie: tokenhere
connection

"""
def main():
    commands = tgtgTesting()
    lines =  sys.stdin.readlines()
    parts = [] 
    for line in lines:
        line = line.strip()
        proccess = line.split(":")[1]
        if proccess == "connection":
            commands.createClient(parts[0], parts[1], parts[2])
            parts = []
            print("ping api")
        elif proccess == "abort":
            commands.abortOrder(parts[0])
            parts = []
        elif proccess == "order":
            commands.orderAnItem(parts[0], parts[1])
            parts = []
        elif proccess == "notify":
            commands.notifyWhenAvaliable(parts[0], parts[1])
            parts = []
        elif proccess == "forceorder":
            commands.notifyWhenAvaliable(parts[0], parts[1])
            parts = []
        else:
            parts.append(proccess)
            

        print(line)


if __name__ == "__main__":
    main()



