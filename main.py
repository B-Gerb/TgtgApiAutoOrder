from tgtg import TgtgClient
import os
from datetime import datetime
import time

def startUp(Email):
    if Email == "skip":
        return createClient()
    client = TgtgClient(email=Email)
    credentials = client.get_credentials()
    if os.path.exists("tokens.txt"):
        os.remove("tokens.txt")
    
    writing = open("tokens.txt", "w")
    writing.write(credentials['access_token'] + "\n")
    writing.write(credentials['refresh_token'] + "\n")
    writing.write(credentials['cookie'] + "\n")
    writing.close()
    return createClient()

def createClient():
    reading = open("tokens.txt", "r")
    access_token = reading.readline().strip()
    refresh_token = reading.readline().strip()
    cookie = reading.readline().strip()
    client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
    return client
def orderItem(item, client):
    print(item['item']['item_id'])
    print(item['store']['store_name'])
    failing = True
    while failing:
        try:
                
            order = client.create_order(item['item']['item_id'], 1)
            successes = False
            print(order)
        except:
            print("Failed to order")
        time.sleep(3)
    print(order)
#If you want to start the client with a new email, use the startUp function
client = startUp(input("Enter your email or type skip of tokens.txt already contains keys: ")) 


items = client.get_items()
possibleOrders = {}
currOrder = 1
for item in items:
    item = client.get_item(item['item']['item_id'])
    if 'pickup_interval' not in item:
        continue 
    startInt = datetime.strptime(item['pickup_interval']['start'], "%Y-%m-%dT%H:%M:%SZ")
    endInt = datetime.strptime(item['pickup_interval']['end'], "%Y-%m-%dT%H:%M:%SZ")
    salesWindow = datetime.strptime(item['next_sales_window_purchase_start'], "%Y-%m-%dT%H:%M:%SZ")
    print(f"Option {currOrder}: At store {item['store']['store_name']} \n" +
        f"Start time: {startInt}, end time: {endInt} ")
    print(f"Next Sales window is at: {salesWindow}")
    possibleOrders[currOrder] = item
    currOrder += 1
order = int(input("Which option would you like to order? "))
orderItem(possibleOrders[order], client)
    



