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
LOCAL
"""
class tgtgCommands:

    def __init__(self, user_timezone=timezone.utc):
        self.timezone = user_timezone
        self.client = None
        self.tokens_path = "tokens.txt"
        self.commands_path = "commands.txt"


    #Token creation is done through users computer not AWS
    def startUp(self, emailToUse):
        if os.path.exists(self.commands_path):
            os.remove(self.commands_path)
            
        if emailToUse == "skip":
            return self.createClient()
        
        try:
            client = TgtgClient(email=emailToUse)
            credentials = client.get_credentials()
            if os.path.exists("tokens.txt"):
                os.remove("tokens.txt")
            with open(self.tokens_path, "w") as writing:
                    writing.write(f"{credentials['access_token']}\n")
                    writing.write(f"{credentials['refresh_token']}\n")
                    writing.write(f"{credentials['cookie']}\n")
                    writing.write(f"{emailToUse}\n")
            self.client = client
            return self.createClient()
        except Exception as e:
            print(f"Failed to create client: {e}")
            sys.exit(1)

    #creates the client
    def createClient(self):
        try:
            # Find the tokens file
            if not os.path.exists(self.tokens_path):
                if os.path.exists(f"src/{self.tokens_path}"):
                    tokens_file = f"src/{self.tokens_path}"
                else:
                    return None
            else:
                tokens_file = self.tokens_path
                
            # Read tokens
            with open(tokens_file, "r") as reading:
                access_token = reading.readline().strip()
                refresh_token = reading.readline().strip()
                cookie = reading.readline().strip()
                
            # Create commands file
            with open(self.commands_path, "w") as writing:
                writing.write(f"channelID:1338537091142778924\n")
                writing.write(f"access_token:{access_token}\n")
                writing.write(f"refresh_token:{refresh_token}\n")
                writing.write(f"cookie:{cookie}\n")
                writing.write("type:connection\n")
                
            # Create client
            self.client = TgtgClient(
                access_token=access_token,
                refresh_token=refresh_token,
                cookie=cookie
            )
            return self.client
            
        except Exception as e:
            print(f"Failed to create client: {e}")
            return None

    #notify if a store is avaliable has option to order
    def creatingNotfication(self, orderOrNot=False):
        if not self.client:
            print("Client not initialized")
            return
        try:
            items = self.client.get_favorites()
            possible_orders = self._display_available_options(items)
            if not possible_orders:
                print("No items found")
                return
            print("_" * 50)
            print("Type *all* to see all possible options or q to quit\n" + 
                  "Type each number separated by a space to choose multiple options")
            action_type = "forceOrder" if orderOrNot else "notify"
            while True:
                user_choice = input(f"Which options would you like to be notified about{' and ordered?' if orderOrNot else '?'}")
                if user_choice == 'q':
                    return
                elif user_choice == "all":
                    self._display_all_options(possible_orders)
                elif user_choice.isdigit() and int(user_choice) in possible_orders:
                    if int(user_choice) not in possible_orders:
                        continue
                        
                    duration = self._get_duration()
                    if duration is None:
                        continue
                        
                    # Write command
                    with open(self.commands_path, "a") as writing:
                        writing.write(f"item_id:{possible_orders[int(user_choice)]['item']['item_id']}\n")
                        writing.write(f"duration:{duration}\n")
                        writing.write(f"type:{action_type}\n")
                    return
                else:
                    parts = user_choice.strip().split()
                    for part in parts:
                        if not part.isdigit() or int(part) not in possible_orders:
                            print("Invalid option")
                            continue
                    print("stores choosen are: ")

                    for part in parts:
                        print(f"{possible_orders[int(part)]['store']['store_name']}")
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
                            allParts += possible_orders[int(part)]['item']['item_id'] + ","
                        allParts = allParts[:-1]
                        writing.write(allParts + "\n")
                        writing.write("duration:" + str(duration) + "\n")
                        writing.write("type:" + ("forceOrder" if orderOrNot else "notify") + "\n")
                        return
        except Exception as e:
            print(f"Error getting items: {e}")
            sys.exit(1)

    def force_order(self):
            self.create_notification(order_or_not=True)


    #order an item with a pickup window and next sale interval
    def orderAnItem(self):
        if not self.client:
            print("Client not initialized")
            return
        try:
            items = self.client.get_favorites()
            possibleOrders = {}
            currOrder = 1
            for item in items:
                item = self.client.get_item(item['item']['item_id'])
                time.sleep(1)
                if'next_sales_window_purchase_start' not in item:
                    continue 
                if 'pickup_interval' not in item:
                    startInt = "No Pickup Interval given"
                    endInt = "No Pickup Interval given"
                else: 
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
                        while (durationTime := input("Duration in minutes: ")):
                            if not durationTime.isdigit():
                                print("Invalid time")
                                continue
                            durationTime = int(durationTime)
                            if durationTime < 0:
                                print("Invalid time'")
                                continue
                            break
                    break
                with open(self.commands_path, "a") as writing:
                        writing.write(f"item_id:{order['item']['item_id']}\n")
                        writing.write(f"duration:{time}\n")
                        writing.write("type:order\n")
        except Exception as e:
            print(f"Error getting items: {e}")
            sys.exit(1)


            
                
    #Helpers
    def _display_available_options(self, items):
        """Return avaliable options from the dictionary"""
        possible_orders = {}
        curr_order = 1
        
        for item in items:
            try:
                possible_orders[curr_order] = item
                print(f"Option {curr_order}: {item['store']['store_name']}")
                curr_order += 1
            except Exception as e:
                print(f"Error getting item details: {e}")
                sys.exit(1)
                
        return possible_orders
    def _get_duration(self):
        while True:
            choice = input("Will check availability for how long in hours? ")
            if not choice.isdigit() or int(choice) < 0:
                print("Invalid time - must be a positive number")
                continue
            return int(choice)


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

    