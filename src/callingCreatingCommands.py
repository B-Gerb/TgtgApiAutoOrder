import requests
import json
import os

AZURE_SERVER = "http://20.84.48.177:5000"

def create_client(email):
    data = {
        "email": email
    }
    response = requests.post(f"{AZURE_SERVER}/new_tokens", json=data)
    return response.json()

def get_stores(access_token, refresh_token, cookie):
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "cookie": cookie
    }
    response = requests.get(f"{AZURE_SERVER}/possible_stores", json=data)
    return response.json()

def main():
    email = input("Enter your email or skip if tokens.txt exists: ")
    if email != "skip":
        data = create_client(email)
        if os.path.exists("tokens.txt"):
            os.remove("tokens.txt")
        with open("tokens.txt", "w") as writing:
            writing.write(data.get("response")['access_token'] + "\n")
            writing.write(data.get("response")['refresh_token'] + "\n")
            writing.write(data.get("response")['cookie'] + "\n")
            access_token = data.get("response")['access_token']
            refresh_token = data.get("response")['refresh_token']
            cookie = data.get("response")['cookie']
        

          

    else:
        with open("tokens.txt", "r") as reading:
            access_token = reading.readline().strip()
            refresh_token = reading.readline().strip()
            cookie = reading.readline().strip()
    stores = get_stores(access_token, refresh_token, cookie)
    print(stores)
        

if __name__ == "__main__":
    main()

