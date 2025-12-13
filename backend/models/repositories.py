"""
Data access layer (repositories) for database operations
FIXED VERSION - Removed async/await (PyMongo is synchronous)
Handles CRUD operations for all collections
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
import logging
from backend.config.database import (
    users_collection,
    analyses_collection,
    reports_collection,
    cost_analyses_collection,
    subscriptions_collection
)
from backend.models.db_models import (
    UserDB, UserAnalysisDB, AuditReportDB, CostAnalysisDB, SubscriptionDB
)

logger = logging.getLogger(__name__)


class UserRepository:
    """User data access operations"""
    
    @staticmethod
    def create(user: UserDB) -> bool:
        """
        Create new user
        
        Args:
            user: UserDB model instance
        
        Returns:
            True if created successfully
        
        Example:
            user = UserDB(user_id="123", email="test@example.com", ...)
            success = UserRepository.create(user)
        """
        try:
            result = users_collection.insert_one(user.dict())
            logger.info(f"✅ User created: {user.email}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create user error: {e}")
            raise
    
    @staticmethod
    def find_by_email(email: str) -> Optional[UserDB]:
        """
        Find user by email
        
        Args:
            email: User's email address
        
        Returns:
            UserDB instance if found, None otherwise
        
        Example:
            user = UserRepository.find_by_email("test@example.com")
            if user:
                print(f"Found user: {user.user_id}")
        """
        try:
            user_data = users_collection.find_one({"email": email})
            if user_data:
                user_data.pop("_id", None)  # Remove MongoDB's _id
                return UserDB(**user_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find by email error: {e}")
            raise
    
    @staticmethod
    def find_by_id(user_id: str) -> Optional[UserDB]:
        """
        Find user by user_id
        
        Args:
            user_id: User's unique ID (UUID)
        
        Returns:
            UserDB instance if found, None otherwise
        
        Example:
            user = UserRepository.find_by_id("550e8400-...")
            if user:
                print(f"User email: {user.email}")
        """
        try:
            user_data = users_collection.find_one({"user_id": user_id})
            if user_data:
                user_data.pop("_id", None)
                return UserDB(**user_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find by ID error: {e}")
            raise
    
    @staticmethod
    def update_last_login(user_id: str) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User's unique ID
        
        Returns:
            True if updated successfully
        
        Example:
            UserRepository.update_last_login("user-123")
        """
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "last_login": datetime.utcnow(),
                        "updated": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update last login error: {e}")
            raise
    
    @staticmethod
    def add_gcp_credentials(
        user_id: str,
        project_id: str,
        encrypted_credentials: str
    ) -> bool:
        """
        Add GCP credentials to user
        
        Args:
            user_id: User's unique ID
            project_id: GCP project ID
            encrypted_credentials: Encrypted service account JSON
        
        Returns:
            True if updated successfully
        
        Example:
            UserRepository.add_gcp_credentials(
                user_id="user-123",
                project_id="my-gcp-project",
                encrypted_credentials="encrypted_string"
            )
        """
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "gcp_project_id": project_id,
                        "gcp_credentials": encrypted_credentials,
                        "updated": datetime.utcnow()
                    }
                }
            )
            logger.info(f"✅ GCP credentials added for user: {user_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Add GCP credentials error: {e}")
            raise
    
    @staticmethod
    def update_subscription(user_id: str, tier: str) -> bool:
        """
        Update user's subscription tier
        
        Args:
            user_id: User's unique ID
            tier: Subscription tier (free, pro, enterprise)
        
        Returns:
            True if updated successfully
        """
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "subscription_tier": tier,
                        "updated": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update subscription error: {e}")
            raise
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """
        Delete user from database
        
        Args:
            user_id: User's unique ID
        
        Returns:
            True if deleted successfully
        
        Warning:
            This is a hard delete. Consider soft delete in production.
        """
        try:
            result = users_collection.delete_one({"user_id": user_id})
            if result.deleted_count > 0:
                logger.info(f"✅ User deleted: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Delete user error: {e}")
            raise


class AnalysisRepository:
    """User analysis data access operations"""
    
    @staticmethod
    def create(analysis: UserAnalysisDB) -> bool:
        """
        Create new analysis
        
        Args:
            analysis: UserAnalysisDB model instance
        
        Returns:
            True if created successfully
        """
        try:
            result = analyses_collection.insert_one(analysis.dict())
            logger.info(f"✅ Analysis created: {analysis.analysis_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create analysis error: {e}")
            raise
    
    @staticmethod
    def find_by_user_id(user_id: str, limit: int = 10) -> List[UserAnalysisDB]:
        """
        Get user's analyses (most recent first)
        
        Args:
            user_id: User's unique ID
            limit: Maximum number of analyses to return
        
        Returns:
            List of UserAnalysisDB instances
        
        Example:
            analyses = AnalysisRepository.find_by_user_id("user-123", limit=5)
            for analysis in analyses:
                print(f"Query: {analysis.query}")
        """
        try:
            analyses_data = list(
                analyses_collection.find({"user_id": user_id})
                .sort("created", -1)  # Most recent first
                .limit(limit)
            )
            analyses = []
            for analysis in analyses_data:
                analysis.pop("_id", None)
                analyses.append(UserAnalysisDB(**analysis))
            return analyses
        except Exception as e:
            logger.error(f"❌ Find analyses error: {e}")
            raise
    
    @staticmethod
    def find_by_id(analysis_id: str) -> Optional[UserAnalysisDB]:
        """
        Find analysis by ID
        
        Args:
            analysis_id: Analysis unique ID
        
        Returns:
            UserAnalysisDB instance if found, None otherwise
        """
        try:
            analysis_data = analyses_collection.find_one({"analysis_id": analysis_id})
            if analysis_data:
                analysis_data.pop("_id", None)
                return UserAnalysisDB(**analysis_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find analysis by ID error: {e}")
            raise
    
    @staticmethod
    def find_recent_by_user(user_id: str, days: int = 30) -> List[UserAnalysisDB]:
        """
        Find analyses from past N days
        
        Args:
            user_id: User's unique ID
            days: Number of days to look back
        
        Returns:
            List of recent UserAnalysisDB instances
        """
        try:
            from datetime import timedelta
            start_date = datetime.utcnow() - timedelta(days=days)
            
            analyses_data = list(
                analyses_collection.find({
                    "user_id": user_id,
                    "created": {"$gte": start_date}
                }).sort("created", -1)
            )
            
            analyses = []
            for analysis in analyses_data:
                analysis.pop("_id", None)
                analyses.append(UserAnalysisDB(**analysis))
            return analyses
        except Exception as e:
            logger.error(f"❌ Find recent analyses error: {e}")
            raise
    
    @staticmethod
    def delete_by_id(analysis_id: str) -> bool:
        """
        Delete analysis by ID
        
        Args:
            analysis_id: Analysis unique ID
        
        Returns:
            True if deleted successfully
        """
        try:
            result = analyses_collection.delete_one({"analysis_id": analysis_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"❌ Delete analysis error: {e}")
            raise
    
    @staticmethod
    def count_by_user(user_id: str) -> int:
        """
        Count total analyses for a user
        
        Args:
            user_id: User's unique ID
        
        Returns:
            Total number of analyses
        """
        try:
            count = analyses_collection.count_documents({"user_id": user_id})
            return count
        except Exception as e:
            logger.error(f"❌ Count analyses error: {e}")
            raise


class AuditReportRepository:
    """Audit report data access operations"""
    
    @staticmethod
    def create(report: AuditReportDB) -> bool:
        """Create new audit report"""
        try:
            result = reports_collection.insert_one(report.dict())
            logger.info(f"✅ Audit report created: {report.report_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create report error: {e}")
            raise
    
    @staticmethod
    def find_by_user_id(user_id: str, limit: int = 10) -> List[AuditReportDB]:
        """Get user's reports (most recent first)"""
        try:
            reports_data = list(
                reports_collection.find({"user_id": user_id})
                .sort("generated_at", -1)
                .limit(limit)
            )
            reports = []
            for report in reports_data:
                report.pop("_id", None)
                reports.append(AuditReportDB(**report))
            return reports
        except Exception as e:
            logger.error(f"❌ Find reports error: {e}")
            raise
    
    @staticmethod
    def find_by_id(report_id: str) -> Optional[AuditReportDB]:
        """Find report by ID"""
        try:
            report_data = reports_collection.find_one({"report_id": report_id})
            if report_data:
                report_data.pop("_id", None)
                return AuditReportDB(**report_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find report error: {e}")
            raise
    
    @staticmethod
    def update_pdf_url(report_id: str, pdf_url: str) -> bool:
        """Update report PDF URL"""
        try:
            result = reports_collection.update_one(
                {"report_id": report_id},
                {
                    "$set": {
                        "pdf_url": pdf_url,
                        "updated": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update PDF URL error: {e}")
            raise


class CostAnalysisRepository:
    """Cost analysis data access operations"""
    
    @staticmethod
    def create(cost_analysis: CostAnalysisDB) -> bool:
        """Create new cost analysis"""
        try:
            result = cost_analyses_collection.insert_one(cost_analysis.dict())
            logger.info(f"✅ Cost analysis created: {cost_analysis.cost_analysis_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create cost analysis error: {e}")
            raise
    
    @staticmethod
    def find_by_user_id(user_id: str, limit: int = 10) -> List[CostAnalysisDB]:
        """Get user's cost analyses"""
        try:
            analyses_data = list(
                cost_analyses_collection.find({"user_id": user_id})
                .sort("analysis_date", -1)
                .limit(limit)
            )
            analyses = []
            for analysis in analyses_data:
                analysis.pop("_id", None)
                analyses.append(CostAnalysisDB(**analysis))
            return analyses
        except Exception as e:
            logger.error(f"❌ Find cost analyses error: {e}")
            raise
    
    @staticmethod
    def find_latest_by_user(user_id: str) -> Optional[CostAnalysisDB]:
        """Get latest cost analysis for user"""
        try:
            analysis_data = cost_analyses_collection.find_one(
                {"user_id": user_id},
                sort=[("analysis_date", -1)]
            )
            if analysis_data:
                analysis_data.pop("_id", None)
                return CostAnalysisDB(**analysis_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find latest cost analysis error: {e}")
            raise


class SubscriptionRepository:
    """Subscription data access operations"""
    
    @staticmethod
    def create(subscription: SubscriptionDB) -> bool:
        """Create new subscription"""
        try:
            result = subscriptions_collection.insert_one(subscription.dict())
            logger.info(f"✅ Subscription created: {subscription.subscription_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create subscription error: {e}")
            raise
    
    @staticmethod
    def find_by_user_id(user_id: str) -> Optional[SubscriptionDB]:
        """Find subscription by user ID"""
        try:
            sub_data = subscriptions_collection.find_one({"user_id": user_id})
            if sub_data:
                sub_data.pop("_id", None)
                return SubscriptionDB(**sub_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find subscription error: {e}")
            raise
    
    @staticmethod
    def update_status(user_id: str, status: str) -> bool:
        """Update subscription status"""
        try:
            result = subscriptions_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "status": status,
                        "updated": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update subscription status error: {e}")
            raise


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Create user
    from backend.models.db_models import UserDB
    
    user = UserDB(
        user_id="test-user-123",
        email="test@example.com",
        password_hash="hashed_password",
        company_name="Test Corp",
        subscription_tier="free",
        created=datetime.utcnow(),
        updated=datetime.utcnow()
    )
    
    # UserRepository.create(user)
    
    # Example 2: Find user
    found_user = UserRepository.find_by_email("test@example.com")
    if found_user:
        print(f"Found: {found_user.email}")
    
    # Example 3: Update last login
    # UserRepository.update_last_login("test-user-123")
    
    # Example 4: Get user's analyses
    # analyses = AnalysisRepository.find_by_user_id("test-user-123")
    # print(f"Total analyses: {len(analyses)}")