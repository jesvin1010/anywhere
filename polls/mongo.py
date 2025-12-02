from pymongo import MongoClient
from datetime import datetime

# -----------------------------------------
# 🔗 CONNECT TO MONGODB (Local Server)
# -----------------------------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    mongo_db = client["activity_db"]               # Database
    activity_logs = mongo_db["user_activity"]      # Collection
except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    client = None
    activity_logs = None

# -----------------------------------------
# ⭐ FUNCTION: Log User Activity
# -----------------------------------------
def log_activity(user, action, details=None):
    """
    Saves activity logs to MongoDB.
    
    user: username (string)
    action: what the user did (string)
    details: extra info (dict or string)
    """

    if activity_logs is None:
        # If MongoDB failed to connect, avoid crashing Django
        print("⚠ Skipping activity log (MongoDB not connected).")
        return

    log_entry = {
        "user": user if user else "Anonymous",
        "action": action,
        "details": details,
        "timestamp": datetime.now()
    }

    try:
        activity_logs.insert_one(log_entry)
    except Exception as e:
        print("❌ Error inserting log:", e)
