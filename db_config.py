from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
import ssl

# Load environment variables
load_dotenv()

def get_database():
    try:
        # Get MongoDB connection string from environment variable
        MONGODB_URI = os.getenv("MONGODB_URI")
        
        # Configure MongoDB client with SSL settings
        client = MongoClient(
            MONGODB_URI,
            tlsCAFile=certifi.where(),
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE
        )
        
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Initialize database and collections
        db = client.email_marketing_db
        
        return db
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Attempting to connect to local MongoDB...")
        
        try:
            # Fallback to local MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client.email_marketing_db
            print("Connected to local MongoDB successfully!")
            return db
        
        except Exception as local_error:
            print(f"Error connecting to local MongoDB: {local_error}")
            raise Exception("Could not connect to any MongoDB instance")

# Initialize database connection
db = get_database()

# Initialize collections
users = db.users
campaigns = db.campaigns
approved_emails = db.approved_emails
strategies = db.strategies

# Create indexes
try:
    users.create_index("email", unique=True)
    campaigns.create_index([("user_id", 1), ("campaign_name", 1)], unique=True)
    print("Database indexes created successfully!")
except Exception as e:
    print(f"Error creating indexes: {e}")
