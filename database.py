from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

try:
    # Connect to MongoDB with SSL certificate verification
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    # Initialize database and collections
    db = client.email_marketing_db
    users = db.users
    campaigns = db.campaigns
    approved_emails = db.approved_emails
    strategies = db.strategies

    # Create indexes
    users.create_index("email", unique=True)
    campaigns.create_index([("user_id", 1), ("campaign_name", 1)], unique=True)

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Fallback to a local MongoDB instance if cloud connection fails
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.email_marketing_db
        users = db.users
        campaigns = db.campaigns
        approved_emails = db.approved_emails
        strategies = db.strategies
        
        # Create indexes
        users.create_index("email", unique=True)
        campaigns.create_index([("user_id", 1), ("campaign_name", 1)], unique=True)
        print("Connected to local MongoDB instance as fallback")
    except Exception as e:
        print(f"Error connecting to local MongoDB: {e}")

# Add these indexes and schema validations
def setup_database_schema():
    try:
        # User collection schema
        db.command({
            'collMod': 'users',
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['email', 'password', 'name', 'created_at'],
                    'properties': {
                        'email': {'bsonType': 'string'},
                        'password': {'bsonType': 'string'},
                        'name': {'bsonType': 'string'},
                        'created_at': {'bsonType': 'date'},
                        'last_login': {'bsonType': 'date'}
                    }
                }
            }
        })

        # Campaign collection schema
        db.command({
            'collMod': 'campaigns',
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['user_id', 'campaign_name', 'created_at'],
                    'properties': {
                        'user_id': {'bsonType': 'string'},
                        'campaign_name': {'bsonType': 'string'},
                        'status': {'enum': ['draft', 'active', 'completed', 'archived']},
                        'created_at': {'bsonType': 'date'},
                        'updated_at': {'bsonType': 'date'}
                    }
                }
            }
        })

        # Create indexes
        users.create_index("email", unique=True)
        campaigns.create_index([("user_id", 1), ("campaign_name", 1)], unique=True)
        campaigns.create_index("user_id")  # For faster user campaign lookups
        
        print("Database schema and indexes created successfully!")
    except Exception as e:
        print(f"Error setting up database schema: {e}")