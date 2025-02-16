from tgtg import TgtgClient
import sys
import os
from datetime import datetime, timezone
import time
import requests

# Class for commands to go through tgtg
class tgtgTesting:
    def __init__(self):
        self.client = None

    # Creates the client
    def createClient(self, access_token, refresh_token, cookie):
        self.client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
        self.notifyUser(type="connection", message="Connection established")

    """
    Returns the order object if successful, otherwise returns "Failed to order"
    item: the item object
    duration: the time in minutes you want to wait to order the item after the next sales window
    """
    def orderAnItem(self, item, duration):
        time = item['next_sales_window_purchase_start']
        target_date = datetime.fromisoformat(time).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        time_to_wait = (target_date - now).total_seconds()
        time.sleep(time_to_wait - 3)
        duration += 3
        firstSpeed = 600
        while firstSpeed > 0:
            order = self.attemptToOrder(item['item']['item_id'], 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("order", order, message="Successful order")
                return
            else:
                time.sleep(1)
                firstSpeed -= 1
        secondSpeed = (duration * 60) - 600
        while secondSpeed > 0:
            order = self.attemptToOrder(item['item']['item_id'], 1)  # Assuming amt=1
            if order != "Failed to order":
                self.notifyUser("order", order, message="Successful order")
                return
            else:
                time.sleep(10)
                secondSpeed -= 10
        self.notifyUser("order", message="Failed to order")

    # Force order an item even if it does not have any available pickup window
    def forceOrder(self, item_id, duration, amt=1):  # Assuming amt=1
        time = duration * 3600
        while time > 0:
            order = self.attemptToOrder(item_id, amt)
            if order != "Failed to order":
                self.notifyUser("forceorder", order, message="Force order placed")
                return
            else:
                time.sleep(10)
                time -= 10

    """
    item_id: the id of the item you want to be notified about
    duration: the time in minutes you want to be notified for in minutes
    """
    def checkAvailable(self, item_id):
        item = self.client.get_item(item_id)
        return item['items_available'] > 0

    def attemptToOrder(self, item_id, amt):
        try:
            order = self.client.create_order(item_id, amt)
            return order
        except:
            return "Failed to order"

    def notifyWhenAvailable(self, item_id, duration):
        duration = duration * 3600
        while duration > 0:
            item = self.client.get_item(item_id)
            if item['items_available'] > 0:
                self.notifyUser("notify", item, "Item is available")
                return
            time.sleep(10)
            duration -= 10
        self.notifyUser("notify", message="Never became available")

    """
    type: the type of notification, either order or notify
    """
    def notifyUser(self, type, item=None, message=None, channelID=None):
        url = "https://tgtgggbot.high5brian.workers.dev/notification"
        if type == "order":
            if item is None:
                #For testing
                data = {
                    "type": "order",
                    "name": "Test",
                    "start": "now",
                    "channelToSend": channelID
                }
            else:
                data = {
                    "type": "order",
                    "name": item['display_name'],  # Example field, adjust as needed
                    "start": item['pickup_interval']['start'].replace(tzinfo=timezone.utc).isoformat(),
                    "channelToSend": channelID
                }
            print("here")
            process = requests.post(url, json=data)
            print(process)
        elif type == "notify":
            print('Placeholder for available')
        elif type == "forceorder":
            print('Placeholder for force order')
        elif type == "connection":
            print('Placeholder for connection')
        elif type == "abort":
            print('Placeholder for abort')
        else:
            return "Invalid type"

    def abortOrder(self, order_id):
        time.sleep(3)
        self.client.abort_order(order_id)
        self.notifyUser("abort", message="Order aborted")


# Main function to handle command-line input
def main():
    commands = tgtgTesting()
    lines = sys.stdin.readlines()
    parts = []
    for line in lines:
        line = line.strip()
        process = line.split(":")[1]
        if process == "connection":
            commands.createClient(parts[0], parts[1], parts[2])
            parts = []
            print("Ping API")
        elif process == "abort":
            commands.abortOrder(parts[0])
            parts = []
        elif process == "order":
            commands.orderAnItem(parts[0], parts[1])
            parts = []
        elif process == "notify":
            commands.notifyWhenAvailable(parts[0], parts[1])
            parts = []
        elif process == "forceorder":
            commands.forceOrder(parts[0], parts[1])
            parts = []
        else:
            parts.append(process)


if __name__ == "__main__":


    main()
