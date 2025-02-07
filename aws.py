import paramiko
from scp import SCPClient
from tgtgClass import tgtgTesting
import os
import sys
from datetime import datetime


def creatingCommands():
    #this will create commands from the user to be executed possible command string
    """
    skip 
    order xyz 3 hours starting at 3:00 5 second intervals notfication system waitTime if confirmed

    """
    setUp = tgtgTesting()
    client = setUp.startUp(input("Enter your email or type skip of tokens.txt already contains keys: ")) 
    items = client.get_items()
    possibleOrders = {}
    currOrder = 1
    for item in items:
        item = client.get_item(item['item']['item_id'])
        if 'pickup_interval' not in item or 'next_sales_window_purchase_start' not in item:
            continue 
        print(item['store']['store_name'])
        startInt = datetime.strptime(item['pickup_interval']['start'], "%Y-%m-%dT%H:%M:%SZ")
        endInt = datetime.strptime(item['pickup_interval']['end'], "%Y-%m-%dT%H:%M:%SZ")
        salesWindow = datetime.strptime(item['next_sales_window_purchase_start'], "%Y-%m-%dT%H:%M:%SZ")
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
            status = setUp.orderItem(possibleOrders[order], client)
            print(client.get_order_status(status['id']))
            print("success hopefully")
            break
            

def ssh_to_ec2(key_path, hostname, username="ubuntu"):
    try:
        # Initialize SSH client
        ssh = paramiko.SSHClient()
        
        # Automatically add host keys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Get the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        # Connect to the EC2 instance
        print(f"Connecting to {hostname}...")
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key
        )
        print("Successfully connected to EC2 instance!")
        scp = SCPClient(ssh.get_transport())

        scp.close()

        stdin,stdout,stderr = ssh.exec_command('python3 -c "print(\'Hello, world!\')"')
        print(stdout.read().decode())   
        

        
    
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH exception occurred: {ssh_exception}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ssh' in locals():
            ssh.close()
            print("SSH connection closed.")

# Your EC2 details
KEY_PATH = "KeyForTesting.pem"
HOSTNAME = "ec2-54-163-195-23.compute-1.amazonaws.com"
USERNAME = "ubuntu"
creatingCommands()  
ssh_to_ec2(KEY_PATH, HOSTNAME, USERNAME)