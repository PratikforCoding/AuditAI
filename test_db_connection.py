# test_db_connection.py
"""Test MongoDB Atlas connection"""

import asyncio
from backend.config.database import DatabaseConnection

async def test_connection():
    try:
        db = DatabaseConnection.get_database()
        print(f"✅ Connected to database: {db.name}")
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✅ Collections: {collections}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Run test
asyncio.run(test_connection())
