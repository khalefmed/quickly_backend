import os
import firebase_admin
from firebase_admin import credentials

# Detect if running on Render or locally
# Render sets this automatically: RENDER=True (or similar)
RUNNING_ON_RENDER = os.getenv("RENDER") is not None

try:
    if not firebase_admin._apps:
        if RUNNING_ON_RENDER:
            # Render → use credentials from environment variable
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("🔥 Firebase initialized with Render credentials")
        else:
            # Local → load from local file
            local_cred_path = "firebase_admin_sdk.json"

            if os.path.exists(local_cred_path):
                cred = credentials.Certificate(local_cred_path)
                firebase_admin.initialize_app(cred)
                print("🔥 Firebase initialized locally using firebase_admin_sdk.json")
            else:
                print("⚠️ Local Firebase credential file missing:", local_cred_path)

except Exception as e:
    print("⚠️ Firebase initialization error:", e)
    pass