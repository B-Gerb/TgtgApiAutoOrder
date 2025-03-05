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
        duration += 3
        firstSpeed = 600
        while firstSpeed > 0:
            order = self.attemptToOrder(item_id, 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                time.sleep(1 + random.uniform(0, .5))
                firstSpeed -= 1
        secondSpeed = (duration * 60) - 600
        while secondSpeed > 0:
            order = self.attemptToOrder(item['item']['item_id'], 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                time.sleep(10 + random.uniform(0, .5))
                secondSpeed -= 10
        self.notifyUser("Failed to order " + name)

    # Force order an item even if it does not have any available pickup window
    def forceOrder(self, item_id, duration, amt=1):  # Assuming amt=1
        item = self.client.get_item(item_id)
        name = item['item']['display_name']
        time = duration * 3600
        while time > 0:
            order = self.attemptToOrder(item_id, amt)
            if order != "Failed to order":
                self.notifyUser("Successful order of " + name)
                return
            else:
                time.sleep(10 + random.uniform(0, .5))
                time -= 10
        self.notifyUser("Failed to order " + name)


    


    """
    item_id: listOfItems
    duration: the time in minutes you want to be notified for in minutes
    """
    def notifyWhenAvailable(self, listOfItems, duration):
        duration = int(duration) * 3600
        while duration > 0:
            for item_id in listOfItems:
                if self.checkAvailable(item_id):
                    item = self.client.get_item(item_id)
                    self.notifyUser(f"Item at store: {item['display_name']} is available")
                    listOfItems.remove(item_id)
                    if len(listOfItems) == 0:
                        return
            time.sleep(10 + random.uniform(0, .5))
            duration -= 10
        names = ""
        for item_id in listOfItems:
            item = self.client.get_item(item_id)
            names += item['display_name'] + ", "
        names = names[:-2]

        self.notifyUser(f"The following store(s) never became became available:{names}")
        
    # Aborts an order
    def abortOrder(self, order_id):
        time.sleep(3)
        self.client.abort_order(order_id)
        self.notifyUser(f"Order for {order_id} has been aborted")


# Main function to handle command-line input
def main():
    commands = tgtgTesting()
    lines = sys.stdin.readlines()
    channelID = lines[0].strip()
    channelID = channelID.split(":")[1]
    commands.setChannelId(channelID)
    lines = lines[1:]
    parts = []
    for line in lines:
        line = line.strip()
        process = line.split(":")[1]
        if process == "connection":
            try:
                commands.createClient(parts[0], parts[1], parts[2])
            except:
                commands.notifyUser("Failed to connect")
            parts = []
            time.sleep(1 + random.uniform(0, .5))
        elif process == "abort":
            try:
                commands.abortOrder(parts[0])
            except:
                commands.notifyUser("Failed to abort")
            parts = []
            time.sleep(1 + random.uniform(0, .5))

        elif process == "order":
            try:
                commands.orderAnItem(parts[0], parts[1])
            except:
                commands.notifyUser("Failed to order")
            parts = []
            time.sleep(1 + random.uniform(0, .5))

        elif process == "notify":
            stores = parts[0].split(",")
            try:
                commands.notifyWhenAvailable(stores, parts[1])
            except:
                commands.notifyUser("Failed to notify")
            parts = []
            time.sleep(1 + random.uniform(0, .5))

        elif process == "forceorder":
            try:
                commands.forceOrder(parts[0], parts[1])
            except:
                commands.notifyUser("Failed to force order")
            parts = []
            time.sleep(1 + random.uniform(0, .5))

        else:
            parts.append(process)


if __name__ == "__main__":


    main()
