from tgtg import TgtgClient
import sys
import os
from datetime import datetime, timezone, timedelta
import time
import requests
import random
# Class for commands to go through tgtg
class tgtgTesting:
    def __init__(self):
        self.client = None
        self.channelID = None
        self.url ="https://tgtgggbot.high5brian.workers.dev/notification"

    def setClient(self, client):
        self.client = client   

    
    def setChannelId(self, channelID):
        self.channelID = channelID

    """
    type: message to send to discord
    """
    def notifyUser(self, message):
        data = {
            "message": message,
            "channelToSend": self.channelID
        }
        process = requests.post(self.url, json=data)
        return process
    # Check if an item is available one time
    def createTime(self, lower, higher):
        return random.uniform(lower, higher)
    def checkAvailable(self, item_id):
        item = self.client.get_item(item_id)
        return item['items_available'] > 0

    # Attempt to order an item
    def attemptToOrder(self, item_id, amt):
        try:
            order = self.client.create_order(item_id, amt)
            return order
        except:
            return "Failed to order"
    
    # Creates the client
    def createClient(self, access_token, refresh_token, cookie):
        self.client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        self.notifyUser("Connection established")

    

    """
    Returns the order object if successful, otherwise returns "Failed to order"
    item: the item object
    duration: the time in minutes you want to wait to order the item after the next sales window
    """
    def orderAnItem(self, item_id, duration):

        item = self.client.get_item(item_id)
        name = item['store']['store_name']
        targetTime = item['next_sales_window_purchase_start']

        target_date = datetime.fromisoformat(targetTime).replace(tzinfo=timezone.utc) - timedelta(hours=5)


        now = datetime.now(timezone.utc) - timedelta(hours=5)

        time_to_wait = (target_date - now).total_seconds()
        time_to_wait = float(time_to_wait)
        time.sleep(time_to_wait - 3)
        if duration.isdigit():
            duration = int(duration)
        else:
            duration += 10
        firstSpeed = 600
        while firstSpeed > 0:
            order = self.attemptToOrder(item_id, 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                sleepTime = self.createTime(1, 5)
                time.sleep(sleepTime)
                firstSpeed -= sleepTime
        secondSpeed = (duration * 60) - 600
        while secondSpeed > 0:
            order = self.attemptToOrder(item['item']['item_id'], 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                sleepTime = self.createTime(20,61)
                time.sleep(sleepTime)
                secondSpeed -= sleepTime
        self.notifyUser("Failed to order " + name)

    # Force order an item even if it does not have any available pickup window
    def forceOrder(self, item_id, duration, amt=1):  # Assuming amt=1
        item = self.client.get_item(item_id)
        name = item['item']['display_name']
        if duration.isdigit():
            duration = int(duration)
        else:
            duration = 10
        waitTime = duration * 3600
        while waitTime > 0:
            order = self.attemptToOrder(item_id, amt)
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                sleepTime = self.createTime(20,61)
                time.sleep(sleepTime)
                waitTime -= sleepTime
        self.notifyUser("Failed to order " + name)


    


    """
    item_id: listOfItems
    duration: the time in minutes you want to be notified for in minutes
    listOfItems: is a set of item_ids a user wants to be notified about
    """
    def notifyWhenAvailable(self, listOfItems, duration):
        if duration.isdigit():
            duration = int(duration)
        else:
            duration = 10
        waitTime = int(duration) * 3600
        listOfItems = set(listOfItems)
        while waitTime > 0:
            try:
                items = self.client.get_favorites()
            except:
                self.notifyUser("Failed to get favorites")
                return
            for item in items:
                if item['item']['item_id'] in listOfItems:
                    if item['items_available'] > 0:
                        self.notifyUser(f"Item at store: {item['display_name']} is available")
                        listOfItems.remove(item['item']['item_id'])
                        if len(listOfItems) == 0:
                            return
            sleepTime = self.createTime(20,61)
            time.sleep(sleepTime)
            waitTime -= sleepTime
        names = ""
        for item_id in listOfItems:
            item = items[item_id]
            names += item['display_name'] + ", "
        names = names[:-2]

        self.notifyUser(f"The following store(s) never became became available:{names}")
        
    # Aborts an order
    def abortOrder(self, order_id):
        time.sleep(3)
        self.client.abort_order(order_id)
        self.notifyUser(f"Order for {order_id} has been aborted")


