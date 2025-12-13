"""
GCP Recommender API Service
UPDATED: Supports per-user credentials
Uses Google Cloud's official recommendation engine
"""

from typing import Dict, List, Optional
from google.cloud import recommender_v1
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GCPRecommenderService:
    """
    Service to fetch official GCP recommendations
    UPDATED: Supports per-user credentials
    """
    
    def __init__(self, project_id: str, user_credentials: Optional[Dict] = None):
        """
        Initialize recommender service
        
        Args:
            project_id: GCP Project ID
            user_credentials: Optional dict with user's service account JSON
                            If None, uses environment credentials (dev mode)
        """
        self.project_id = project_id
        self.parent = f"projects/{project_id}/locations/global"
        
        try:
            # Initialize recommender client with credentials
            if user_credentials:
                logger.info(f"🔒 Using user credentials for recommender service: {project_id}")
                
                credentials = service_account.Credentials.from_service_account_info(
                    user_credentials,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                
                self.client = recommender_v1.RecommenderClient(credentials=credentials)
            else:
                logger.info(f"🔧 Using environment credentials for recommender service: {project_id}")
                
                self.client = recommender_v1.RecommenderClient()
            
            logger.info(f"✅ Recommender service initialized for project: {project_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize recommender service: {e}")
            raise
        
    def get_idle_resource_recommendations(self) -> List[Dict]:
        """
        Get official GCP recommendations for idle resources
        Uses: google.compute.instance.IdleResourceRecommender
        """
        try:
            recommendations = self._fetch_recommendations(
                'google.compute.instance.IdleResourceRecommender'
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
                    'recommender': 'google.compute.instance.IdleResourceRecommender',
                    'actions': self._extract_actions(rec),
                    'state': str(rec.state)
                })
            
            logger.info(f"Found {len(formatted)} idle resource recommendations")
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching idle resource recommendations: {e}")
            return []
    
    def get_oversized_instance_recommendations(self) -> List[Dict]:
        """
        Get GCP recommendations for oversized instances
        Uses: google.compute.instance.MachineTypeRecommender
        """
        try:
            recommendations = self._fetch_recommendations(
                'google.compute.instance.MachineTypeRecommender'
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
                    'recommender': 'google.compute.instance.MachineTypeRecommender',
                    'current_machine_type': self._extract_machine_type(rec),
                    'actions': self._extract_actions(rec),
                    'state': str(rec.state)
                })
            
            logger.info(f"Found {len(formatted)} resize recommendations")
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching resize recommendations: {e}")
            return []
    
    def get_disk_recommendations(self) -> List[Dict]:
        """
        Get GCP recommendations for disk optimization
        Uses: google.compute.disk.IdleResourceRecommender
        """
        try:
            recommendations = self._fetch_recommendations(
                'google.compute.disk.IdleResourceRecommender'
            )
            
            formatted = []
            for rec in recommendations:
                primary_impact = rec.primary_impact
                estimated_savings = self._extract_savings(primary_impact)
                
                formatted.append({
                    'recommendation_id': rec.name.split('/')[-1],
                    'resource_id': self._extract_resource_id(rec),
                    'title': 'Delete Idle Disk',
                    'description': rec.description,
                    'severity': self._map_recommender_priority(rec.priority),
                    'estimated_annual_savings': estimated_savings,
                    'monthly_savings': estimated_savings / 12,
                    'confidence': rec.priority,
                    'recommender': 'google.compute.disk.IdleResourceRecommender',
                    'actions': self._extract_actions(rec),
                    'state': str(rec.state)
                })
            
            logger.info(f"Found {len(formatted)} disk recommendations")
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching disk recommendations: {e}")
            return []
    
    def get_storage_recommendations(self) -> List[Dict]:
        """Get GCP recommendations for storage optimization"""
        try:
            recommendations = self._fetch_recommendations(
                'google.storage.bucket.AccessControlRecommender'
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
                    'recommender': 'google.storage.bucket.AccessControlRecommender',
                    'actions': self._extract_actions(rec),
                    'state': str(rec.state)
                })
            
            logger.info(f"Found {len(formatted)} storage recommendations")
            return formatted
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching storage recommendations: {e}")
            return []
    
    def get_all_recommendations(self) -> List[Dict]:
        """Get all active recommendations from GCP Recommender"""
        try:
            all_recommendations = []
            
            # Add all recommender types
            all_recommendations.extend(self.get_idle_resource_recommendations())
            all_recommendations.extend(self.get_oversized_instance_recommendations())
            all_recommendations.extend(self.get_disk_recommendations())
            all_recommendations.extend(self.get_storage_recommendations())
            
            logger.info(f"Total recommendations found: {len(all_recommendations)}")
            return all_recommendations
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching all recommendations: {e}")
            return []
    
    def mark_recommendation_claimed(self, recommendation_id: str, recommender_type: str):
        """Mark recommendation as claimed (user acknowledged it)"""
        try:
            name = f"{self.parent}/recommenders/{recommender_type}/recommendations/{recommendation_id}"
            self.client.mark_recommendation_claimed(name=name)
            logger.info(f"Marked recommendation {recommendation_id} as claimed")
        except GoogleCloudError as e:
            logger.error(f"Error marking recommendation as claimed: {e}")
            raise
    
    def mark_recommendation_succeeded(self, recommendation_id: str, recommender_type: str):
        """Mark recommendation as succeeded (user acted on it)"""
        try:
            name = f"{self.parent}/recommenders/{recommender_type}/recommendations/{recommendation_id}"
            self.client.mark_recommendation_succeeded(name=name)
            logger.info(f"Marked recommendation {recommendation_id} as succeeded")
        except GoogleCloudError as e:
            logger.error(f"Error marking recommendation as succeeded: {e}")
            raise
    
    def verify_recommender_access(self) -> bool:
        """
        Verify that Recommender API is accessible
        Returns True if we can query recommendations
        """
        try:
            parent = f"{self.parent}/recommenders/google.compute.instance.IdleResourceRecommender"
            request = recommender_v1.ListRecommendationsRequest(
                parent=parent,
                page_size=1
            )
            list(self.client.list_recommendations(request=request))
            
            logger.info("✅ Recommender API access verified")
            return True
            
        except Exception as e:
            logger.error(f"❌ Recommender API access verification failed: {e}")
            return False
    
    # ========================================================================
    # Private helper methods
    # ========================================================================
    
    def _fetch_recommendations(self, recommender_id: str) -> List:
        """Fetch recommendations from specific recommender"""
        try:
            parent = f"{self.parent}/recommenders/{recommender_id}"
            request = recommender_v1.ListRecommendationsRequest(
                parent=parent,
                filter='stateInfo.state="ACTIVE"'  # Get active recommendations
            )
            response = self.client.list_recommendations(request=request)
            return list(response)
        except GoogleCloudError as e:
            logger.warning(f"Could not fetch recommendations for {recommender_id}: {e}")
            return []
    
    def _extract_savings(self, primary_impact) -> float:
        """Extract cost savings from impact"""
        if not primary_impact:
            return 0.0
        
        try:
            if hasattr(primary_impact, 'cost_projection'):
                if hasattr(primary_impact.cost_projection, 'cost'):
                    cost = primary_impact.cost_projection.cost
                    if hasattr(cost, 'units'):
                        return abs(float(cost.units))
                    elif hasattr(cost, 'nanos'):
                        return abs(float(cost.nanos) / 1_000_000_000)
        except Exception as e:
            logger.warning(f"Error extracting savings: {e}")
        
        return 0.0
    
    def _extract_resource_id(self, recommendation) -> str:
        """Extract resource ID from recommendation"""
        try:
            if hasattr(recommendation, 'target_resources') and recommendation.target_resources:
                # Resource format: //compute.googleapis.com/projects/PROJECT/zones/ZONE/instances/INSTANCE
                resource = recommendation.target_resources[0]
                parts = resource.split('/')
                return parts[-1]  # Return last part (resource name)
        except Exception as e:
            logger.warning(f"Error extracting resource ID: {e}")
        
        return 'unknown'
    
    def _extract_machine_type(self, recommendation) -> str:
        """Extract current machine type from recommendation"""
        try:
            if hasattr(recommendation, 'content'):
                content = recommendation.content
                if hasattr(content, 'overview'):
                    overview = content.overview
                    if 'currentMachineType' in overview:
                        return overview['currentMachineType']
        except Exception as e:
            logger.warning(f"Error extracting machine type: {e}")
        
        return 'unknown'
    
    def _extract_actions(self, recommendation) -> List[Dict]:
        """Extract recommended actions"""
        actions = []
        try:
            if hasattr(recommendation, 'content') and recommendation.content:
                content = recommendation.content
                if hasattr(content, 'operation_groups'):
                    for op_group in content.operation_groups:
                        for operation in op_group.operations:
                            actions.append({
                                'action': operation.action if hasattr(operation, 'action') else 'unknown',
                                'resource': operation.resource if hasattr(operation, 'resource') else 'unknown',
                                'resource_type': operation.resource_type if hasattr(operation, 'resource_type') else 'unknown'
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
        
        if hasattr(priority, 'name'):
            priority_str = priority.name
        else:
            priority_str = str(priority).split('.')[-1] if priority else 'P4'
        
        return priority_map.get(priority_str, 'MEDIUM')


# Usage example:
if __name__ == "__main__":
    import os
    import json
    
    project_id = os.getenv("GOOGLE_PROJECT_ID", "test-project")
    
    # Test with environment credentials
    service = GCPRecommenderService(project_id)
    
    if service.verify_recommender_access():
        print("✅ Recommender service is ready!")
        
        # Get all recommendations
        recommendations = service.get_all_recommendations()
        print(f"Found {len(recommendations)} recommendations")
        
        if recommendations:
            print("\nSample recommendation:")
            print(json.dumps(recommendations[0], indent=2))
    else:
        print("❌ Recommender service verification failed")