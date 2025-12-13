"""
Data access layer (repositories) for database operations
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
    async def create(user: UserDB) -> bool:
        """Create new user"""
        try:
            result = users_collection.insert_one(user.dict())
            logger.info(f"✅ User created: {user.email}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create user error: {e}")
            raise
    
    @staticmethod
    async def find_by_email(email: str) -> Optional[UserDB]:
        """Find user by email"""
        try:
            user_data = users_collection.find_one({"email": email})
            if user_data:
                user_data.pop("_id", None)
                return UserDB(**user_data)
            return None
        except Exception as e:
            logger.error(f"❌ Find by email error: {e}")
            raise
    
    @staticmethod
    async def find_by_id(user_id: str) -> Optional[UserDB]:
        """Find user by user_id"""
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
    async def update_last_login(user_id: str) -> bool:
        """Update last login timestamp"""
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "last_login": datetime.utcnow().isoformat(),
                        "updated": datetime.utcnow().isoformat()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update last login error: {e}")
            raise
    
    @staticmethod
    async def add_gcp_credentials(
        user_id: str,
        project_id: str,
        encrypted_credentials: str
    ) -> bool:
        """Add GCP credentials to user"""
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "gcp_project_id": project_id,
                        "gcp_credentials": encrypted_credentials,
                        "updated": datetime.utcnow().isoformat()
                    }
                }
            )
            logger.info(f"✅ GCP credentials added for user: {user_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Add GCP credentials error: {e}")
            raise
    
    @staticmethod
    async def update_subscription(user_id: str, tier: str) -> bool:
        """Update user subscription tier"""
        try:
            result = users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "subscription_tier": tier,
                        "updated": datetime.utcnow().isoformat()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update subscription error: {e}")
            raise


class AnalysisRepository:
    """User analysis data access operations"""
    
    @staticmethod
    async def create(analysis: UserAnalysisDB) -> bool:
        """Create new analysis"""
        try:
            result = analyses_collection.insert_one(analysis.dict())
            logger.info(f"✅ Analysis created: {analysis.analysis_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create analysis error: {e}")
            raise
    
    @staticmethod
    async def find_by_user_id(user_id: str, limit: int = 10) -> List[UserAnalysisDB]:
        """Get user's analyses"""
        try:
            analyses_data = list(
                analyses_collection.find({"user_id": user_id})
                .sort("created", -1)
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
    async def find_by_id(analysis_id: str) -> Optional[UserAnalysisDB]:
        """Find analysis by ID"""
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
    async def find_recent_by_user(user_id: str, days: int = 30) -> List[UserAnalysisDB]:
        """Find recent analyses by user"""
        try:
            from datetime import timedelta
            start_date = datetime.utcnow() - timedelta(days=days)
            
            analyses_data = list(
                analyses_collection.find({
                    "user_id": user_id,
                    "created": {"$gte": start_date.isoformat()}
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
    async def delete_by_id(analysis_id: str) -> bool:
        """Delete analysis by ID"""
        try:
            result = analyses_collection.delete_one({"analysis_id": analysis_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"❌ Delete analysis error: {e}")
            raise


class AuditReportRepository:
    """Audit report data access operations"""
    
    @staticmethod
    async def create(report: AuditReportDB) -> bool:
        """Create new audit report"""
        try:
            result = reports_collection.insert_one(report.dict())
            logger.info(f"✅ Audit report created: {report.report_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create report error: {e}")
            raise
    
    @staticmethod
    async def find_by_user_id(user_id: str, limit: int = 10) -> List[AuditReportDB]:
        """Get user's reports"""
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
    async def find_by_id(report_id: str) -> Optional[AuditReportDB]:
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
    async def update_pdf_url(report_id: str, pdf_url: str) -> bool:
        """Update report PDF URL"""
        try:
            result = reports_collection.update_one(
                {"report_id": report_id},
                {
                    "$set": {
                        "pdf_url": pdf_url,
                        "updated": datetime.utcnow().isoformat()
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
    async def create(cost_analysis: CostAnalysisDB) -> bool:
        """Create new cost analysis"""
        try:
            result = cost_analyses_collection.insert_one(cost_analysis.dict())
            logger.info(f"✅ Cost analysis created: {cost_analysis.cost_analysis_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create cost analysis error: {e}")
            raise
    
    @staticmethod
    async def find_by_user_id(user_id: str, limit: int = 10) -> List[CostAnalysisDB]:
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
    async def find_latest_by_user(user_id: str) -> Optional[CostAnalysisDB]:
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
    async def create(subscription: SubscriptionDB) -> bool:
        """Create new subscription"""
        try:
            result = subscriptions_collection.insert_one(subscription.dict())
            logger.info(f"✅ Subscription created: {subscription.subscription_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"❌ Create subscription error: {e}")
            raise
    
    @staticmethod
    async def find_by_user_id(user_id: str) -> Optional[SubscriptionDB]:
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
    async def update_status(user_id: str, status: str) -> bool:
        """Update subscription status"""
        try:
            result = subscriptions_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "status": status,
                        "updated": datetime.utcnow().isoformat()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update subscription status error: {e}")
            raise