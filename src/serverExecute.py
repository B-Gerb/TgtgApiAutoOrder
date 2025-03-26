import requests
import json
import sys
import os
import time
AZURE_SERVER = "http://20.84.48.177:5000"
#Server


def executeCommand(filePath):
    if os.path.exists(filePath):
        file = open(filePath, "r")
    elif os.path.exists(f"src/{filePath}"):
        file = open(f"src/{filePath}", "r")
    else:
        print("File not found")
        return
    file = file.readlines()
    data = {}
    for line in file:
        key, value = line.split(":")
        data[key] = value

    requests.post(f"{AZURE_SERVER}/execute_command", json=data, timeout=5)
    print("Command executed")
    return


executeCommand('commands.txt')