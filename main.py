from tgtg import TgtgClient
import os
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
#If you want to start the client with a new email, use the startUp function
client = startUp(input("Enter your email or type skip of tokens.txt already contains keys: ")) 


items = client.get_items()
for item in items:
     print(item['store']['store_name'])