import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load .env file
load_dotenv()

# Get token from environment
uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a Database
db = client["HRChatbot"]

# Create a collection
collection = db["candidate_info"]
    
def insert_data(data):    
    # Insert the data to the collection
    inserted_data = collection.insert_one(data)
    
    return insert_data