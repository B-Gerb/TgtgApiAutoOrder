import requests
import json
import os
import sys
from datetime import datetime, timezone

AZURE_SERVER = "http://20.84.48.177:5000"
AWS_SERVER = "http://54.242.239.216:5000"
HOME_SERVER = "http://127.0.0.1:5000"

class TgtgServerClient:
    def __init__(self, user_timezone=timezone.utc):
        self.timezone = user_timezone
        self.tokens_path = "tokens.txt"
        self.commands_path = "commands.txt"
        self.access_token = None
        self.refresh_token = None
        self.cookie = None
        self.email = None
        self.server = None

    def set_server(self, server):
        self.server = server

    def startup(self, email):
        if os.path.exists(self.commands_path):
            os.remove(self.commands_path)
            
        if email == "skip":
            return self.load_tokens()
        
        try:
            response = self.create_client(email)
            if "response" in response:
                credentials = response["response"]
                if os.path.exists(self.tokens_path):
                    os.remove(self.tokens_path)
                with open(self.tokens_path, "w") as writing:
                    writing.write(f"{credentials['access_token']}\n")
                    writing.write(f"{credentials['refresh_token']}\n")
                    writing.write(f"{credentials['cookie']}\n")
                    writing.write(f"{email}\n")
                
                self.access_token = credentials['access_token']
                self.refresh_token = credentials['refresh_token']
                self.cookie = credentials['cookie']
                self.email = email
                
                # Create commands file
                with open(self.commands_path, "w") as writing:
                    writing.write(f"channelID:1338537091142778924\n")
                    writing.write(f"access_token:{self.access_token}\n")
                    writing.write(f"refresh_token:{self.refresh_token}\n")
                    writing.write(f"cookie:{self.cookie}\n")
                    writing.write("type:connection\n")
                
                return True
            else:
                print(f"Failed to create client: {response.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Failed to create client: {e}")
            return False
        
    def load_tokens(self):

        try:
            if not os.path.exists(self.tokens_path):
                if os.path.exists(f"src/{self.tokens_path}"):
                    tokens_file = f"src/{self.tokens_path}"
                else:
                    print("No tokens file found")
                    return False
            else:
                tokens_file = self.tokens_path
                
            # Read tokens
            with open(tokens_file, "r") as reading:
                self.access_token = reading.readline().strip()
                self.refresh_token = reading.readline().strip()
                self.cookie = reading.readline().strip()
                self.email = reading.readline().strip() if reading.readline() else "unknown"
                
            # Create commands file
            with open(self.commands_path, "w") as writing:
                writing.write(f"channelID:1338537091142778924\n")
                writing.write(f"access_token:{self.access_token}\n")
                writing.write(f"refresh_token:{self.refresh_token}\n")
                writing.write(f"cookie:{self.cookie}\n")
                writing.write("type:connection\n")
                
            return True
            
        except Exception as e:
            print(f"Failed to load tokens: {e}")
            return False
        
    def create_client(self, email):
        data = {
            "email": email
        }
        if not self.server:
            print("Server not set")
            return None
        try:
            response = requests.post(f"{self.server}/new_tokens", json=data)
            return response.json()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit(1)

    def get_stores(self):
        if not self.server:
            print("Server not set")
            return None
        if not self.access_token or not self.refresh_token or not self.cookie:
            print("Client not initialized properly")
            return None
            
        data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "cookie": self.cookie
        }
        try:
            print("attempting to get stores")
            response = requests.get(f"{self.server}/possible_stores", json=data)
            return response.json()
        except Exception as e:
            print(f"Error getting stores: {e}")
            return None
    
    #duration in minutes
    def create_order(self, item_id, duration):
        if not self.access_token:
            print("Client not initialized properly")
            return False
            
        with open(self.commands_path, "a") as writing:
            writing.write(f"item_id:{item_id}\n")
            writing.write(f"duration:{duration}\n")
            writing.write("type:order\n")
        return True
    
    #duration in hours
    def create_notification(self, item_ids, duration, order_or_not=False):
        if not self.access_token:
            print("Client not initialized properly")
            return False
            
        action_type = "forceOrder" if order_or_not else "notify"
        
        with open(self.commands_path, "a") as writing:
            if isinstance(item_ids, list):
                writing.write(f"item_id:{','.join(item_ids)}\n")
            else:
                writing.write(f"item_id:{item_ids}\n")
            writing.write(f"duration:{duration}\n")
            writing.write(f"type:{action_type}\n")
        return True

    def display_available_options(self, stores):
        """Display available options from the list of stores"""
        if not stores or not 'stores' in stores:
            print("No stores available!!!")
            return {}
            
        possible_orders = {}
        curr_order = 1
        
        for store in stores['stores']:
            try:
                store_name = store.get('display_name', "Unknown Name")
                store_id = store.get('item', {}).get('item_id', "Unknown ID")
                if store_id == "Unknown ID":
                    continue
                possible_orders[curr_order] = {"item_id": store_id, "store_name": store_name}
                print(f"Option {curr_order}: {store_name}")
                curr_order += 1
            except Exception as e:
                print(f"Error displaying store: {e}")
                
        return possible_orders
    
    def get_duration(self, order=False):
        while True:
            choice = input(f"Will check availability for how long in {'minutes' if order else 'hours'}? ")
            if not choice.isdigit() or int(choice) < 0:
                print("Invalid time - must be a positive number")
                continue
            return int(choice)




            
def create_commands(server=None, notification=False, order=False, force_order=False):
    if server is None:
        print("Server not specified")
        return
    

    amountOfTrue = 0
    if notification:
        amountOfTrue += 1
    if order:
        amountOfTrue += 1
    if force_order:
        amountOfTrue += 1
    if amountOfTrue > 1:
        print("Can only have one type of action")
        return
    client = TgtgServerClient()
    client.set_server(server)  
    email = input("Enter your email or type skip if tokens.txt already contains keys: ")
    
    if not client.startup(email):
        print("Failed to initialize client")
        return
    
    stores = client.get_stores()
    runTimes = 1
    while 'error' in stores:
        stringerror = stores['error']
        start_index = stringerror.find('"url":"') + len('"url":"')
        end_index = stringerror.find('"', start_index)
        url = stringerror[start_index:end_index]
        print(url)
        input()  # checkpoint to wait for manual captcha completion ( I press enter in the console to continue the script)
        stores = client.get_stores()
        if runTimes > 3:
            print("Failed to get stores")
            return
        runTimes += 1


    possible_orders = client.display_available_options(stores)
    
    if not possible_orders:
        print("No stores available")
        return
        
    print("_" * 50)
    print("Type 'all' to see all possible options or 'q' to quit\n" + 
          "Type each number separated by a space to choose multiple options\n" +
          "Can only order/force order one store at a time")
    if order:
        action = 'order'
    elif force_order:
        action = 'force order'
    else:
        action = 'notify'
    while True:
        user_choice = input(f"Which options would you like to {action}? ")
        
        if user_choice.lower() == 'q':
            return
        elif user_choice.lower() == "all":
            for position in possible_orders:
                print(f"Option {position}: {possible_orders[position]['store_name']}")
            print("_" * 50)
            continue
        elif user_choice.isdigit() and int(user_choice) in possible_orders:
            choice = int(user_choice)
            print(f"Selected store: {possible_orders[choice]['store_name']}")
            
            if input("To confirm this store type y, to cancel type anything else: ") != 'y':
                continue
                
            duration = client.get_duration(order=order)
            
            if order:
                client.create_order(possible_orders[choice]['item_id'], duration)
            else:
                client.create_notification(possible_orders[choice]['item_id'], duration, order_or_not=force_order)
            
            print("Command created successfully!")
            return
        else:
            parts = user_choice.strip().split()
            valid_parts = []
            
            for part in parts:
                if not part.isdigit() or int(part) not in possible_orders:
                    print(f"Invalid option: {part}")
                    break
                valid_parts.append(part)
                
            if len(valid_parts) != len(parts):
                continue
                
            print("Stores chosen are: ")
            for part in valid_parts:
                choice = int(part)
                print(f"{possible_orders[choice]['store_name']}")
                
            if input("To confirm these stores type y, to cancel type anything else: ") != 'y':
                continue
                
            duration = client.get_duration()
            
            item_ids = [possible_orders[int(part)]['item_id'] for part in valid_parts]
            
            if order or force_order:
                print("Cannot order from multiple stores at once")
                continue
            else:
                client.create_notification(item_ids, duration, order_or_not=force_order)
                
            print("Command created successfully!")
            return

            

if __name__ == "__main__":
    inputOption = input("Do you want to execute through aws, azure, or home? (aws/azure/home): ")
    if inputOption == "aws":
        server = AWS_SERVER
    elif inputOption == "azure":
        server = AZURE_SERVER
    elif inputOption == "home":
        server = HOME_SERVER
    else:
        print("Invalid option")
        sys.exit(1)

    create_commands(notification=True, server=server)

