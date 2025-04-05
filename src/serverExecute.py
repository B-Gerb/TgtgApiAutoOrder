import requests
import json
import sys
import os
import time

AZURE_SERVER = "http://20.84.48.177:5000"
AWS_SERVER = "http://54.242.239.216:5000"
#Server


def executeCommand(filePath, server):
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

    requests.post(f"{server}/execute_command", json=data)
    print("Command executed")
    return


inputOption = input("Do you want to execute through aws or azure? (aws/azure): ")
if inputOption == "aws":
    server = AWS_SERVER
elif inputOption == "azure":
    server = AZURE_SERVER

executeCommand('commands.txt', server)