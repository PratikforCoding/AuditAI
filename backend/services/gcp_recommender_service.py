"""
GCP Recommender API Service
Uses Google Cloud's official recommendation engine
"""

from typing import Dict, List, Optional
from google.cloud import recommender_v1
from google.cloud.exceptions import GoogleCloudError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GCPRecommenderService:
    """Service to fetch official GCP recommendations"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = recommender_v1.RecommenderClient()
        self.parent = f"projects/{project_id}/locations/global"
        
    def get_idle_resource_recommendations(self) -> List[Dict]:
        """
        Get official GCP recommendations for idle resources
        Uses: compute.instances.idleResources recommender
        """
        try:
            recommendations = self._fetch_recommendations(
                'compute.instances.idleResources'
            )
            
            formatted = []
            for rec in recommendations:
                # GCP provides official primary and secondary impacts
                primary_impact = rec.primary_impact
                estimated_savings = self._extract_savings(primary_impact)
                
                formatted.append({
                    'recommendation_id': rec.name.split('/')[-1],
                    'resource_id': self._extract_resource_id(rec),
                    'title': 'Idle Compute Instance',
                    'description': rec.description,
                    'severity': self._map_recommender_priority(rec.priority),
                    'estimated_annual_savings': estimated_savings,
                    'monthly_savings': estimated_savings / 12,
                    'confidence': rec.priority,  # GCP's confidence level
                    'recommender': 'compute.instances.idleResources',
                    'actions': self._extract_actions(rec)
                })
            
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching idle resource recommendations: {e}")
            raise
    
    def get_oversized_instance_recommendations(self) -> List[Dict]:
        """
        Get GCP recommendations for oversized instances
        Uses: compute.instances.changeType recommender
        """
        try:
            recommendations = self._fetch_recommendations(
                'compute.instances.changeType'
            )
            
            formatted = []
            for rec in recommendations:
                primary_impact = rec.primary_impact
                estimated_savings = self._extract_savings(primary_impact)
                
                formatted.append({
                    'recommendation_id': rec.name.split('/')[-1],
                    'resource_id': self._extract_resource_id(rec),
                    'title': 'Resize Compute Instance',
                    'description': rec.description,
                    'severity': self._map_recommender_priority(rec.priority),
                    'estimated_annual_savings': estimated_savings,
                    'monthly_savings': estimated_savings / 12,
                    'confidence': rec.priority,
                    'recommender': 'compute.instances.changeType',
                    'current_machine_type': rec.content.target_resources if rec.content.target_resources else 'Unknown',
                    'actions': self._extract_actions(rec)
                })
            
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching resize recommendations: {e}")
            raise
    
    def get_storage_recommendations(self) -> List[Dict]:
        """Get GCP recommendations for storage optimization"""
        try:
            recommendations = self._fetch_recommendations(
                'storage.buckets.denyUnauthenticatedPublicRead'
            )
            
            formatted = []
            for rec in recommendations:
                primary_impact = rec.primary_impact
                # Storage security recommendations don't have cost savings
                estimated_savings = self._extract_savings(primary_impact)
                
                formatted.append({
                    'recommendation_id': rec.name.split('/')[-1],
                    'resource_id': self._extract_resource_id(rec),
                    'title': 'Secure Storage Bucket',
                    'description': rec.description,
                    'severity': self._map_recommender_priority(rec.priority),
                    'estimated_annual_savings': estimated_savings or 0,
                    'monthly_savings': (estimated_savings or 0) / 12,
                    'confidence': rec.priority,
                    'recommender': 'storage.buckets.denyUnauthenticatedPublicRead',
                    'actions': self._extract_actions(rec)
                })
            
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching storage recommendations: {e}")
            raise
    
    def get_all_recommendations(self) -> List[Dict]:
        """Get all active recommendations from GCP Recommender"""
        try:
            all_recommendations = []
            
            # Add all recommender types
            all_recommendations.extend(self.get_idle_resource_recommendations())
            all_recommendations.extend(self.get_oversized_instance_recommendations())
            all_recommendations.extend(self.get_storage_recommendations())
            
            return all_recommendations
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching all recommendations: {e}")
            raise
    
    def mark_recommendation_claimed(self, recommendation_id: str):
        """Mark recommendation as claimed (user acknowledged it)"""
        try:
            name = f"{self.parent}/recommenders/compute.instances.idleResources/recommendations/{recommendation_id}"
            self.client.mark_recommendation_claimed(name=name)
            logger.info(f"Marked recommendation {recommendation_id} as claimed")
        except GoogleCloudError as e:
            logger.error(f"Error marking recommendation as claimed: {e}")
            raise
    
    def mark_recommendation_succeeded(self, recommendation_id: str):
        """Mark recommendation as succeeded (user acted on it)"""
        try:
            name = f"{self.parent}/recommenders/compute.instances.idleResources/recommendations/{recommendation_id}"
            self.client.mark_recommendation_succeeded(name=name)
            logger.info(f"Marked recommendation {recommendation_id} as succeeded")
        except GoogleCloudError as e:
            logger.error(f"Error marking recommendation as succeeded: {e}")
            raise
    
    # Private helper methods
    
    def _fetch_recommendations(self, recommender_id: str) -> List:
        """Fetch recommendations from specific recommender"""
        parent = f"{self.parent}/recommenders/{recommender_id}"
        request = recommender_v1.ListRecommendationsRequest(
            parent=parent,
            filter='state != "CLAIMED"'  # Get active recommendations
        )
        response = self.client.list_recommendations(request=request)
        return list(response)
    
    def _extract_savings(self, primary_impact) -> float:
        """Extract cost savings from impact"""
        if not primary_impact:
            return 0.0
        
        try:
            if hasattr(primary_impact, 'cost_projection'):
                if hasattr(primary_impact.cost_projection, 'cost'):
                    return abs(float(primary_impact.cost_projection.cost.units))
        except Exception as e:
            logger.warning(f"Error extracting savings: {e}")
        
        return 0.0
    
    def _extract_resource_id(self, recommendation) -> str:
        """Extract resource ID from recommendation"""
        try:
            if recommendation.target_resources:
                # Resource format: projects/PROJECT/zones/ZONE/instances/INSTANCE
                resource = recommendation.target_resources
                parts = resource.split('/')
                return parts[-1]  # Return last part (resource name)
        except Exception as e:
            logger.warning(f"Error extracting resource ID: {e}")
        
        return 'unknown'
    
    def _extract_actions(self, recommendation) -> List[Dict]:
        """Extract recommended actions"""
        actions = []
        try:
            if hasattr(recommendation, 'recommended_actions'):
                for action in recommendation.recommended_actions:
                    actions.append({
                        'action': action.action,
                        'description': action.description
                    })
        except Exception as e:
            logger.warning(f"Error extracting actions: {e}")
        
        return actions
    
    def _map_recommender_priority(self, priority) -> str:
        """Map GCP priority to severity"""
        priority_map = {
            'P1': 'CRITICAL',
            'P2': 'HIGH',
            'P3': 'MEDIUM',
            'P4': 'LOW',
        }
        priority_str = str(priority).split('.')[-1] if priority else 'P4'
        return priority_map.get(priority_str, 'MEDIUM')
