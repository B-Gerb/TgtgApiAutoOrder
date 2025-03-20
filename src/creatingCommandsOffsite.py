from tgtg import TgtgClient
from flask import Flask, request, jsonify
from tgtg import TgtgClient
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
created_clients = {}



class TgtgHandler:
    def __init__(self):
        self.client = None

    def create_client(self, access_token, refresh_token, cookie):
        try:
            self.client = TgtgClient(access_token=access_token, refresh_token=refresh_token, cookie=cookie)
            return True
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            return False
    
    def create_new_client(self, email):
        try:
            self.client = TgtgClient(email=email)
            credentials = self.client.get_credentials()
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
def delete_client():
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

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
       