"""
MongoDB Atlas connection and initialization
Handles all database operations and collections
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from contextlib import contextmanager
from typing import Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """MongoDB Atlas connection manager"""
    
    _instance = None
    _client: Optional[MongoClient] = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def connect(cls):
        """Establish MongoDB Atlas connection"""
        try:
            cls._client = MongoClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True,
                w="majority"
            )
            
            # Verify connection
            cls._client.admin.command('ping')
            cls._database = cls._client[settings.DATABASE_NAME]
            
            logger.info(f"✅ Connected to MongoDB Atlas: {settings.DATABASE_NAME}")
            
            # Create indexes
            cls._create_indexes()
            
            return cls._database
            
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            logger.error(f"❌ Failed to connect to MongoDB Atlas: {e}")
            raise
    
    @classmethod
    def _create_indexes(cls):
        """Create database indexes for performance"""
        try:
            db = cls._database
            
            # Users collection indexes
            db.users.create_index("email", unique=True)
            db.users.create_index("user_id", unique=True)
            db.users.create_index("created")
            
            # User analyses indexes
            db.user_analyses.create_index([("user_id", 1), ("created", -1)])
            db.user_analyses.create_index("analysis_id", unique=True)
            db.user_analyses.create_index("project_id")
            
            # Audit reports indexes
            db.audit_reports.create_index([("user_id", 1), ("generated_at", -1)])
            db.audit_reports.create_index("report_id", unique=True)
            
            # Cost analyses indexes
            db.cost_analyses.create_index([("user_id", 1), ("analysis_date", -1)])
            db.cost_analyses.create_index("project_id")
            
            # Subscriptions indexes
            db.subscriptions.create_index("user_id", unique=True)
            db.subscriptions.create_index("status")
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        if cls._database is None:
            cls.connect()
        return cls._database
    
    @classmethod
    def disconnect(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            logger.info("✅ MongoDB connection closed")
    
    @classmethod
    def health_check(cls) -> bool:
        """Check database health"""
        try:
            cls._client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return False


# Initialize database connection
db = DatabaseConnection.get_database()


@contextmanager
def get_db_session():
    """Context manager for database operations"""
    try:
        yield db
    except Exception as e:
        logger.error(f"Database operation error: {e}")
        raise
    finally:
        pass


# Collection references
users_collection = db.users
analyses_collection = db.user_analyses
reports_collection = db.audit_reports
cost_analyses_collection = db.cost_analyses
subscriptions_collection = db.subscriptions