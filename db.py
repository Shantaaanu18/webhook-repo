from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
import os

# Get MongoDB connection string from environment variable or use default
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Please ensure MongoDB is running and accessible")
    client = None

db = client["github_events"] if client is not None else None
events_collection = db["events"] if db is not None else None

def insert_event(event):
    if events_collection is None:
        print("Warning: MongoDB not connected, event not saved")
        return False
    
    try:
        event["timestamp"] = datetime.utcnow()
        result = events_collection.insert_one(event)
        print(f"Event saved with ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error saving event to MongoDB: {e}")
        return False

def get_latest_events(limit=10):
    if events_collection is None:
        print("Warning: MongoDB not connected, returning empty list")
        return []
    
    try:
        return list(events_collection.find().sort("timestamp", -1).limit(limit))
    except Exception as e:
        print(f"Error fetching events from MongoDB: {e}")
        return []
