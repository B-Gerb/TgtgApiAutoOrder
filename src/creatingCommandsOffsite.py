from tgtg import TgtgClient
from flask import Flask, request, jsonify
from tgtg import TgtgClient
import logging
import os
import tgtgClass
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
created_clients = {}
emails = {}


class TgtgHandler:
    def __init__(self):
        self.client = None

    def create_client(self, access_token, refresh_token, cookie):
        try:
            if((access_token, refresh_token, cookie) in created_clients):
                self.client = created_clients[(access_token, refresh_token, cookie)]
                return created_clients[(access_token, refresh_token, cookie)]
            else:
                self.client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
                created_clients[(access_token, refresh_token, cookie)] = self.client
            return True
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            return False
    
    def remove_client(self, access_token, refresh_token, cookie):
        if (access_token, refresh_token, cookie) in created_clients:
            del created_clients[(access_token, refresh_token, cookie)]
            return True
        else:
            return False
    
    def create_new_client(self, email):
        try:
            self.client = TgtgClient(email=email)
            credentials = self.client.get_credentials()
            emails[email] = (credentials['access_token'], credentials['refresh_token'], credentials['cookie'])
            created_clients[(credentials['access_token'], credentials['refresh_token'], credentials['cookie'])] = self.client
            return credentials
        except Exception as e:
            logger.error(f"Error creating new client: {str(e)}")
            return None
    
    def possible_stores(self):
        if not self.client:
            return {"error": "Client not initialized"}
        try:
            stores = self.client.get_favorites()
            return stores
        except Exception as e:
            logger.error(f"Error getting stores: {str(e)}")
            return {"error": str(e)}
        

@app.route('/new_tokens', methods=['POST'])
def create_client():
    data = request.json
    email = data.get('email')
    handler = TgtgHandler()
    response = handler.create_new_client(email)
    return jsonify({"response": response})

@app.route('/delete', methods=['POST'])
def removeEmail():
    data = request.json
    email = data.get('email')
    if email in created_clients:
        del created_clients[email]
        return jsonify({"response": "Deleted"})
    else:
        return jsonify({"response: Not found"}), 

@app.route('/possible_stores', methods=['GET'])
def possible_stores():
    handler = TgtgHandler()
    data = request.json
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    cookie = data.get('cookie')
    result = handler.create_client(access_token, refresh_token, cookie)
    if not result:
        return jsonify({"error": "Failed to create client"}), 500
    result = handler.possible_stores()

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500
    else:
        return jsonify({"status": "Success", "stores": result})
@app.route('/remove_client', methods=['POST'])
def delete_client():
    handler = TgtgHandler()
    data = request.json
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    cookie = data.get('cookie')
    result = handler.delete_client(access_token, refresh_token, cookie)
    if result:
        return jsonify({"status": "Success"})
    else:
        return jsonify({"status": "Failed to delete client"}), 500
    

@app.route('/execute_command', methods=['POST'])
def execute_command():
    handler = TgtgHandler()
    data = request.json
    access_token = data.get('access_token').strip()
    refresh_token = data.get('refresh_token').strip()
    cookie = data.get('cookie').strip()
    discord_channel = data.get('channelID').strip()
    result = handler.create_client(access_token, refresh_token, cookie)
    if not result:
        return jsonify({"error": "Failed to create client"}), 500
    executer = tgtgClass.tgtgTesting()
    executer.setClient(handler.client)
    executer.setChannelId(discord_channel)
    stores = data.get('item_id').strip()
    commands = data.get('type').strip()
    duration = data.get('duration').strip()
    stores = stores.strip().split(",")
    print(commands, stores, duration)
    if commands == 'notify':
        executer.notifyUser("Starting to notify")
        result = executer.notifyWhenAvailable(stores, duration)
    elif commands == 'order':
        executer.notifyUser("Starting to order")

        result = executer.orderAnItem(stores[0], duration)
    elif commands == 'forceorder':
        executer.notifyUser("Starting to force order")

        result = executer.forceOrder(stores[0], duration)
    elif commands == 'abort':
        result = executer.abortOrder(stores[0])
    else:
        return jsonify({"error": "Invalid command"}), 400


    return jsonify(result)
if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
       