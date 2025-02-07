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
            try:    
                order = self.client.create_order(item['item']['item_id'], 1)
                notifyUser("order", order, message= "successful order")
                return
            except:
                time.sleep(1)
                firstSpeed -= 1
        secondSpeed = (duration*60) - 600
        while secondSpeed > 0:
            try:    
                order = self.client.create_order(item['item']['item_id'], 1)
                notifyUser("order", order, message= "successful order")
                return
            except:
                time.sleep(10)
                secondSpeed -= 1
        notifyUser("order", message= "Failed to order")
         


    """
    item_id: the id of the item you want to be notified about
    duration: the time in minutes you want to be notified for in minutes
    """
    def notifyWhenAvaliable(self, item_id, duration):
        duration = duration*60

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
        elif type == "connection":
            print('place holder for connection')
        elif type == "abort":
            print('place holder for abort')
        else:
            return "Invalid type"

    def abortOrder(self, order_id):
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
    lines =  sys.stdin.readlines()
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()



