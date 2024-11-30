from database import campaigns, approved_emails, strategies
from datetime import datetime
from bson import ObjectId

def save_campaign(user_id: str, campaign_data: dict):
    """Save a new campaign or update existing one"""
    campaign = {
        "user_id": user_id,
        "campaign_name": campaign_data["campaign_name"],
        "product_name": campaign_data["product_name"],
        "target_audience": campaign_data["target_audience"],
        "campaign_goal": campaign_data["campaign_goal"],
        "timeline": campaign_data["timeline"],
        "num_emails": campaign_data["num_emails"],
        "frequency": campaign_data["frequency"],
        "email_tone": campaign_data["email_tone"],
        "template_style": campaign_data["template_style"],
        "status": "draft",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = campaigns.update_one(
        {"user_id": user_id, "campaign_name": campaign_data["campaign_name"]},
        {"$set": campaign},
        upsert=True
    )
    
    return str(result.upserted_id) if result.upserted_id else None

def save_strategy(campaign_id: str, strategy_text: str):
    """Save campaign strategy"""
    strategy = {
        "campaign_id": campaign_id,
        "strategy_text": strategy_text,
        "created_at": datetime.utcnow()
    }
    return strategies.insert_one(strategy).inserted_id

def save_approved_email(campaign_id: str, email_data: dict):
    """Save an approved email"""
    email = {
        "campaign_id": campaign_id,
        "email_number": email_data["email_number"],
        "subject": email_data["subject"],
        "content": email_data["content"],
        "feedback": email_data.get("feedback", ""),
        "approved_at": datetime.utcnow()
    }
    return approved_emails.insert_one(email).inserted_id

def verify_user_campaign_access(user_id: str, campaign_id: str) -> bool:
    """Verify user has access to campaign"""
    campaign = campaigns.find_one({
        "_id": ObjectId(campaign_id),
        "user_id": user_id
    })
    return campaign is not None

def get_user_campaigns(user_id: str):
    """Get all campaigns for a user"""
    try:
        if not user_id:
            print("Error: user_id is None")
            return []
            
        user_id_str = str(user_id)
        pipeline = [
            {
                "$match": {
                    "user_id": user_id_str
                }
            },
            {
                "$lookup": {
                    "from": "approved_emails",
                    "localField": "_id",
                    "foreignField": "campaign_id",
                    "as": "emails"
                }
            },
            {
                "$sort": {"created_at": -1}
            }
        ]
        
        return list(campaigns.aggregate(pipeline))
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return []

def get_campaign_details(campaign_id: str):
    """Get complete campaign details including strategy and approved emails"""
    campaign = campaigns.find_one({"_id": ObjectId(campaign_id)})
    if not campaign:
        return None
    
    strategy = strategies.find_one({"campaign_id": campaign_id})
    emails = list(approved_emails.find({"campaign_id": campaign_id}).sort("email_number", 1))
    
    return {
        "campaign": campaign,
        "strategy": strategy["strategy_text"] if strategy else None,
        "approved_emails": emails
    }

def update_campaign_status(campaign_id: str, status: str):
    """Update campaign status"""
    campaigns.update_one(
        {"_id": ObjectId(campaign_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )

def verify_database_connection():
    """Verify database connection and campaign collection"""
    try:
        # Test database connection
        campaigns.database.client.admin.command('ping')
        
        # Count total campaigns
        total_campaigns = campaigns.count_documents({})
        
        # Get a sample campaign
        sample_campaign = campaigns.find_one()
        
        return {
            "status": "connected",
            "total_campaigns": total_campaigns,
            "sample_campaign": sample_campaign
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
