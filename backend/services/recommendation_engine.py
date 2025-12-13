"""
Production-Ready Recommendation Engine
UPDATED: Supports per-user credentials
Combines GCP APIs with domain expertise
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging
from enum import Enum

from models.schemas import Recommendation
from services.gcp_billing_service import GCPBillingService
from services.gcp_monitoring_service import GCPMonitoringService
from services.gcp_recommender_service import GCPRecommenderService

logger = logging.getLogger(__name__)


class RecommendationType(str, Enum):
    IDLE_RESOURCE = "idle_resource"
    OVERSIZED_RESOURCE = "oversized_resource"
    UNUSED_DISK = "unused_disk"
    SECURITY_ISSUE = "security_issue"
    COST_OPTIMIZATION = "cost_optimization"


class Severity(str, Enum):
    """Severity levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProductionRecommendationEngine:
    """
    Production-grade recommendation engine using official GCP APIs
    All recommendations are based on actual data, not guesses
    UPDATED: Supports per-user credentials
    """
    
    def __init__(self, project_id: str, user_credentials: Optional[Dict] = None):
        """
        Initialize recommendation engine
        
        Args:
            project_id: GCP Project ID
            user_credentials: Optional dict with user's service account JSON
        """
        self.project_id = project_id
        self.user_credentials = user_credentials
        
        # Initialize services with user credentials
        self.billing_service = GCPBillingService(project_id, user_credentials)
        self.monitoring_service = GCPMonitoringService(project_id, user_credentials)
        self.recommender_service = GCPRecommenderService(project_id, user_credentials)
        
        # Thresholds based on industry standards and GCP best practices
        self.IDLE_CPU_THRESHOLD = 5.0  # % utilization
        self.IDLE_DAYS_THRESHOLD = 30  # days of <5% utilization
        self.MIN_MONTHLY_SAVINGS = 10.0  # Don't recommend if savings < $10/month
        
    def analyze_infrastructure(self, days: int = 30) -> List[Dict]:
        """
        Complete analysis using official GCP data
        Returns high-confidence recommendations with real numbers
        """
        recommendations = []
        
        try:
            # Step 1: Get official GCP recommendations
            logger.info("Fetching official GCP recommendations...")
            try:
                gcp_recs = self.recommender_service.get_all_recommendations()
                recommendations.extend(self._convert_gcp_recommendations(gcp_recs))
            except Exception as e:
                logger.error(f"Failed to fetch GCP recommendations: {e}")
            
            # Step 2: Get actual costs
            logger.info("Fetching billing data...")
            try:
                cost_data = self.billing_service.get_project_total_cost(days=30)
                logger.info(f"Project costs: ${cost_data.get('total_cost', 0)} in last 30 days")
            except Exception as e:
                logger.error(f"Failed to fetch cost data: {e}")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error analyzing infrastructure: {e}")
            raise
    
    def _convert_gcp_recommendations(self, gcp_recs: List[Dict]) -> List[Dict]:
        """Convert official GCP recommendations to our schema"""
        recommendations = []
        
        for rec in gcp_recs:
            monthly_savings = rec.get('monthly_savings', 0)
            
            # Only include recommendations with meaningful savings
            if monthly_savings < self.MIN_MONTHLY_SAVINGS:
                logger.debug(f"Skipping {rec['title']} - savings ${monthly_savings} < minimum")
                continue
            
            # Determine risk level based on action type
            risk_level = self._calculate_risk_level(rec)
            
            # Create recommendation with real data
            recommendation = {
                "id": str(uuid.uuid4()),
                "resource_id": rec.get('resource_id', 'unknown'),
                "title": rec['title'],
                "description": rec['description'],
                "recommendation_type": self._classify_recommendation(rec),
                "severity": self._determine_severity(rec, monthly_savings),
                "monthly_savings": monthly_savings,
                "annual_savings": rec.get('estimated_annual_savings', 0),
                "confidence": self._map_confidence(rec.get('confidence')),
                "risk_level": risk_level,
                "difficulty": self._determine_difficulty(rec),
                "action_items": rec.get('actions', []),
                "source": 'GCP Recommender API',
                "recommender_id": rec.get('recommender', 'unknown'),
                "created_at": datetime.utcnow().isoformat(),
                "data_source": 'production_api'
            }
            
            recommendations.append(recommendation)
            logger.info(f"Added recommendation: {recommendation['title']} | Savings: ${monthly_savings}/month")
        
        return recommendations
    
    def _classify_recommendation(self, rec: Dict) -> str:
        """Classify recommendation type based on recommender"""
        recommender = rec.get('recommender', '')
        
        if 'idle' in recommender.lower():
            return RecommendationType.IDLE_RESOURCE
        elif 'changeType' in recommender:
            return RecommendationType.OVERSIZED_RESOURCE
        elif 'storage' in recommender.lower():
            return RecommendationType.SECURITY_ISSUE
        else:
            return RecommendationType.COST_OPTIMIZATION
    
    def _determine_severity(self, rec: Dict, monthly_savings: float) -> str:
        """
        Determine severity based on:
        1. GCP's confidence
        2. Potential monthly savings
        """
        # GCP's priority is our primary indicator
        gcp_severity = rec.get('severity', 'MEDIUM')
        monthly_savings = monthly_savings or 0
        
        # Map GCP severity + savings to our severity scale
        if gcp_severity == 'CRITICAL' or monthly_savings > 1000:
            return Severity.CRITICAL.value
        elif gcp_severity == 'HIGH' or monthly_savings > 500:
            return Severity.HIGH.value
        elif gcp_severity == 'MEDIUM' or monthly_savings > 100:
            return Severity.MEDIUM.value
        else:
            return Severity.LOW.value
    
    def _calculate_risk_level(self, rec: Dict) -> str:
        """
        Risk of implementing this recommendation
        Based on action type and resource criticality
        """
        title = rec.get('title', '').lower()
        
        # Deleting resources = HIGH risk (data loss potential)
        if 'delete' in title or 'remove' in title:
            return Severity.HIGH.value
        
        # Resizing/modifying = MEDIUM risk (downtime, performance)
        elif 'resize' in title or 'change' in title or 'modify' in title:
            return Severity.MEDIUM.value
        
        # Security fixes = LOW risk (no downtime)
        else:
            return Severity.LOW.value
    
    def _determine_difficulty(self, rec: Dict) -> str:
        """
        Difficulty to implement recommendation
        """
        title = rec.get('title', '').lower()
        
        if 'secure' in title or 'security' in title:
            return 'Easy'  # Usually just config change
        elif 'delete' in title:
            return 'Medium'  # Requires backup, data export
        elif 'resize' in title:
            return 'Medium'  # Requires downtime planning
        else:
            return 'Hard'
    
    def _map_confidence(self, gcp_confidence) -> float:
        """Map GCP confidence level to 0-1 scale"""
        confidence_map = {
            'P1': 0.95,
            'P2': 0.85,
            'P3': 0.75,
            'P4': 0.60,
        }
        
        confidence_str = str(gcp_confidence).split('.')[-1] if gcp_confidence else 'P4'
        return confidence_map.get(confidence_str, 0.70)
    
    def get_cost_analysis(self) -> Dict:
        """Get detailed cost analysis"""
        try:
            total_cost = self.billing_service.get_project_total_cost(days=30)
            cost_by_service = self.billing_service.get_cost_by_service(days=30)
            cost_trend = self.billing_service.get_cost_trend(days=90)
            
            return {
                'total_cost': total_cost,
                'by_service': cost_by_service,
                'trend': cost_trend,
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting cost analysis: {e}")
            raise
    
    def get_recommendations_summary(self) -> Dict:
        """Get summary of all recommendations"""
        try:
            recommendations = self.analyze_infrastructure()
            
            total_monthly_savings = sum(
                r.get('monthly_savings', 0) for r in recommendations
            )
            total_annual_savings = sum(
                r.get('annual_savings', 0) for r in recommendations
            )
            
            by_severity = {}
            for severity in Severity:
                count = len([
                    r for r in recommendations 
                    if r.get('severity') == severity.value
                ])
                if count > 0:
                    by_severity[severity.value] = count
            
            return {
                'total_recommendations': len(recommendations),
                'total_monthly_savings': round(total_monthly_savings, 2),
                'total_annual_savings': round(total_annual_savings, 2),
                'by_severity': by_severity,
                'recommendations': recommendations,
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            raise