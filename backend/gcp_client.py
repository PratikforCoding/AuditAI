"""
Complete GCPClient implementation with all required methods
Add these methods to your existing gcp_client.py file
"""

from google.cloud import billing_v1
from google.cloud import monitoring_v3
from google.cloud import recommender_v1
from google.cloud.monitoring_v3 import query
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class GCPClient:
    """
    Complete GCP Client with all API integrations
    """
    
    def __init__(self, project_id: str, service_account_info: Optional[Dict] = None):
        """
        Initialize GCP Client
        
        Args:
            project_id: GCP Project ID
            service_account_info: Service account JSON as dict (optional)
        """
        self.project_id = project_id
        self.service_account_info = service_account_info
        
        # Initialize credentials
        if service_account_info:
            from google.oauth2 import service_account
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=[
                    'https://www.googleapis.com/auth/cloud-platform',
                    'https://www.googleapis.com/auth/compute.readonly',
                    'https://www.googleapis.com/auth/devstorage.read_only',
                ]
            )
        else:
            # Use default credentials (from environment)
            from google.auth import default
            self.credentials, _ = default()
        
        # Initialize clients
        self._init_clients()
    
    def _init_clients(self):
        """Initialize all GCP service clients"""
        from google.cloud import compute_v1, storage
        
        self.compute_client = compute_v1.InstancesClient(credentials=self.credentials)
        self.storage_client = storage.Client(
            project=self.project_id,
            credentials=self.credentials
        )
        
        # Initialize other clients (will be created on-demand)
        self._billing_client = None
        self._monitoring_client = None
        self._recommender_client = None
    
    @property
    def billing_client(self):
        """Lazy-load billing client"""
        if self._billing_client is None:
            self._billing_client = billing_v1.CloudBillingClient(
                credentials=self.credentials
            )
        return self._billing_client
    
    @property
    def monitoring_client(self):
        """Lazy-load monitoring client"""
        if self._monitoring_client is None:
            self._monitoring_client = monitoring_v3.MetricServiceClient(
                credentials=self.credentials
            )
        return self._monitoring_client
    
    @property
    def recommender_client(self):
        """Lazy-load recommender client"""
        if self._recommender_client is None:
            self._recommender_client = recommender_v1.RecommenderClient(
                credentials=self.credentials
            )
        return self._recommender_client
    
    # ========================================================================
    # EXISTING METHODS (Keep your current implementation)
    # ========================================================================
    
    def verify_credentials(self) -> bool:
        """
        Verify that credentials are valid
        FAST version - just checks if we can authenticate
        """
        try:
            # Simplest possible check - just verify we can create a client
            from google.cloud import compute_v1
            
            # Try to create a zones client - this validates credentials without API calls
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            
            # Make a single lightweight request with pagination limit
            request = compute_v1.ListZonesRequest(
                project=self.project_id,
                max_results=1
            )
            
            # Try to get just one zone
            zones_iterator = zones_client.list(request=request)
            
            # Force evaluation but don't iterate through all results
            try:
                first_zone = next(iter(zones_iterator), None)
                if first_zone:
                    logger.info(f"✅ Credentials verified - can access project {self.project_id}")
                    return True
                else:
                    logger.warning("⚠️ No zones found but credentials work")
                    return True  # Credentials work, just no zones
            except StopIteration:
                # No zones but credentials are valid
                return True
            
        except Exception as e:
            logger.error(f"❌ Credential verification failed: {e}")
            return False
    
    def fetch_compute_instances(self) -> List[Dict]:
        """
        Fetch compute engine instances
        OPTIMIZED: Only checks common zones to avoid timeout
        """
        try:
            from google.cloud import compute_v1
            
            instances = []
            
            # Only check common zones instead of listing all zones
            # This prevents the slow "list all zones" API call
            common_zones = [
                # US zones
                'us-central1-a', 'us-central1-b', 'us-central1-c',
                'us-east1-b', 'us-east1-c', 'us-east1-d',
                'us-west1-a', 'us-west1-b',
                # Europe zones
                'europe-west1-b', 'europe-west1-c', 'europe-west1-d',
                'europe-west2-a', 'europe-west2-b',
                # Asia zones
                'asia-south1-a', 'asia-south1-b', 'asia-south1-c',  # Mumbai (India)
                'asia-south2-a', 'asia-south2-b', 'asia-south2-c',  # Delhi (India)
                'asia-southeast1-a', 'asia-southeast1-b',  # Singapore
                'asia-east1-a', 'asia-east1-b',  # Taiwan
                'asia-northeast1-a', 'asia-northeast1-b',  # Tokyo
            ]
            
            logger.info(f"Checking {len(common_zones)} common zones for instances")
            
            # Fetch instances from common zones only
            for zone_name in common_zones:
                try:
                    request = compute_v1.ListInstancesRequest(
                        project=self.project_id,
                        zone=zone_name,
                        max_results=100  # Limit results per zone
                    )
                    zone_instances = self.compute_client.list(request=request)
                    
                    for instance in zone_instances:
                        instances.append({
                            'name': instance.name,
                            'zone': zone_name,
                            'machine_type': instance.machine_type.split('/')[-1] if instance.machine_type else 'unknown',
                            'status': instance.status,
                            'creation_timestamp': instance.creation_timestamp,
                            'id': str(instance.id) if hasattr(instance, 'id') else None
                        })
                
                except Exception as e:
                    # Zone might not exist in this project or no permission
                    # This is expected, just skip
                    logger.debug(f"Skipping zone {zone_name}: {str(e)[:100]}")
                    continue
            
            logger.info(f"✅ Fetched {len(instances)} compute instances from {len(common_zones)} zones")
            return instances
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch compute instances: {e}")
            raise
    
    def fetch_storage_buckets(self) -> List[Dict]:
        """Fetch cloud storage buckets"""
        try:
            buckets = []
            for bucket in self.storage_client.list_buckets():
                buckets.append({
                    'name': bucket.name,
                    'location': bucket.location,
                    'storage_class': bucket.storage_class,
                    'created': bucket.time_created.isoformat() if bucket.time_created else None
                })
            
            logger.info(f"Fetched {len(buckets)} storage buckets")
            return buckets
            
        except Exception as e:
            logger.error(f"Failed to fetch storage buckets: {e}")
            raise
    
    # ========================================================================
    # NEW METHODS - Add these to your GCPClient
    # ========================================================================
    
    def fetch_billing_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Fetch billing data for the project
        
        Args:
            days: Number of days to fetch billing data for
            
        Returns:
            Dictionary containing billing information
        """
        try:
            logger.info(f"Fetching billing data for last {days} days")
            
            # Get billing account info
            project_name = f"projects/{self.project_id}"
            
            try:
                project_billing_info = self.billing_client.get_project_billing_info(
                    name=project_name
                )
                
                billing_enabled = project_billing_info.billing_enabled
                billing_account = project_billing_info.billing_account_name
                
            except Exception as e:
                logger.warning(f"Could not fetch billing info: {e}")
                billing_enabled = False
                billing_account = None
            
            # Note: To get actual cost data, you need BigQuery with billing export enabled
            # This is a basic implementation that checks if billing is enabled
            
            result = {
                "project_id": self.project_id,
                "billing_enabled": billing_enabled,
                "billing_account": billing_account,
                "period_days": days,
                "message": "Billing data available" if billing_enabled else "Billing not enabled",
                "note": "For detailed cost analysis, enable BigQuery billing export in your GCP project"
            }
            
            logger.info(f"Billing data fetched: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch billing data: {e}")
            raise
    
    def fetch_resource_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """
        Fetch resource metrics from Cloud Monitoring
        
        Args:
            hours: Number of hours to fetch metrics for
            
        Returns:
            Dictionary containing resource metrics
        """
        try:
            logger.info(f"Fetching resource metrics for last {hours} hours")
            
            project_name = f"projects/{self.project_id}"
            
            # Define time interval
            now = datetime.utcnow()
            interval = monitoring_v3.TimeInterval(
                {
                    "end_time": {"seconds": int(now.timestamp())},
                    "start_time": {"seconds": int((now - timedelta(hours=hours)).timestamp())},
                }
            )
            
            metrics_data = {}
            
            # Fetch CPU utilization metrics for compute instances
            try:
                cpu_filter = 'metric.type="compute.googleapis.com/instance/cpu/utilization"'
                
                results = self.monitoring_client.list_time_series(
                    request={
                        "name": project_name,
                        "filter": cpu_filter,
                        "interval": interval,
                        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                    }
                )
                
                cpu_metrics = []
                for result in results:
                    instance_id = result.resource.labels.get('instance_id', 'unknown')
                    zone = result.resource.labels.get('zone', 'unknown')
                    
                    # Get average value
                    if result.points:
                        values = [point.value.double_value for point in result.points]
                        avg_cpu = sum(values) / len(values) if values else 0
                        
                        cpu_metrics.append({
                            'instance_id': instance_id,
                            'zone': zone,
                            'avg_cpu_utilization': round(avg_cpu * 100, 2),  # Convert to percentage
                            'data_points': len(values)
                        })
                
                metrics_data['cpu_utilization'] = cpu_metrics
                logger.info(f"Fetched CPU metrics for {len(cpu_metrics)} instances")
                
            except Exception as e:
                logger.warning(f"Failed to fetch CPU metrics: {e}")
                metrics_data['cpu_utilization'] = []
            
            # Fetch memory utilization (if available)
            try:
                memory_filter = 'metric.type="compute.googleapis.com/instance/memory/utilization"'
                
                results = self.monitoring_client.list_time_series(
                    request={
                        "name": project_name,
                        "filter": memory_filter,
                        "interval": interval,
                        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                    }
                )
                
                memory_metrics = []
                for result in results:
                    instance_id = result.resource.labels.get('instance_id', 'unknown')
                    
                    if result.points:
                        values = [point.value.double_value for point in result.points]
                        avg_memory = sum(values) / len(values) if values else 0
                        
                        memory_metrics.append({
                            'instance_id': instance_id,
                            'avg_memory_utilization': round(avg_memory * 100, 2),
                            'data_points': len(values)
                        })
                
                metrics_data['memory_utilization'] = memory_metrics
                logger.info(f"Fetched memory metrics for {len(memory_metrics)} instances")
                
            except Exception as e:
                logger.warning(f"Failed to fetch memory metrics: {e}")
                metrics_data['memory_utilization'] = []
            
            result = {
                "project_id": self.project_id,
                "period_hours": hours,
                "metrics": metrics_data,
                "timestamp": now.isoformat()
            }
            
            logger.info(f"Resource metrics fetched successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch resource metrics: {e}")
            raise
    
    def fetch_recommendations(self, recommender_type: str = "google.compute.instance.MachineTypeRecommender") -> List[Dict[str, Any]]:
        """
        Fetch recommendations from GCP Recommender API
        OPTIMIZED: Only checks a few zones to avoid timeout
        
        Args:
            recommender_type: Type of recommender to query
            
        Returns:
            List of recommendations
        """
        try:
            logger.info(f"Fetching recommendations of type: {recommender_type}")
            
            recommendations = []
            
            # Only check a few key zones instead of all zones
            # This prevents timeout on the recommender API
            priority_zones = [
                'us-central1-a',
                'us-east1-b',
                'europe-west1-b',
                'asia-south1-a',  # Mumbai
                'asia-south2-a',  # Delhi
                'asia-southeast1-a',  # Singapore
            ]
            
            logger.info(f"Checking {len(priority_zones)} priority zones for recommendations")
            
            for zone in priority_zones:
                try:
                    parent = f"projects/{self.project_id}/locations/{zone}/recommenders/{recommender_type}"
                    
                    # List recommendations for this location
                    request = recommender_v1.ListRecommendationsRequest(
                        parent=parent,
                        page_size=10  # Limit to 10 per zone
                    )
                    response = self.recommender_client.list_recommendations(request=request)
                    
                    for recommendation in response:
                        recommendations.append({
                            'name': recommendation.name,
                            'description': recommendation.description,
                            'recommender_subtype': recommendation.recommender_subtype,
                            'priority': recommendation.priority.name if recommendation.priority else 'UNKNOWN',
                            'state': recommendation.state.name if recommendation.state else 'UNKNOWN',
                            'location': zone,
                            'primary_impact': {
                                'category': recommendation.primary_impact.category.name if recommendation.primary_impact else 'UNKNOWN',
                                'cost_projection': {
                                    'cost': recommendation.primary_impact.cost_projection.cost.units if recommendation.primary_impact and recommendation.primary_impact.cost_projection else 0,
                                    'duration': str(recommendation.primary_impact.cost_projection.duration) if recommendation.primary_impact and recommendation.primary_impact.cost_projection else 'Unknown'
                                } if recommendation.primary_impact else None
                            },
                            'last_refresh_time': recommendation.last_refresh_time.isoformat() if recommendation.last_refresh_time else None
                        })
                
                except Exception as zone_error:
                    # Zone might not have any recommendations or API not available
                    logger.debug(f"No recommendations in zone {zone}: {str(zone_error)[:100]}")
                    continue
            
            logger.info(f"✅ Fetched {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch recommendations: {e}")
            raise
    
    def get_cost_analysis_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get a comprehensive cost analysis summary
        Combines billing data with resource information
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Cost analysis summary
        """
        try:
            logger.info(f"Generating cost analysis summary for {days} days")
            
            # Fetch billing info
            billing_data = self.fetch_billing_data(days=days)
            
            # Fetch resources
            instances = self.fetch_compute_instances()
            buckets = self.fetch_storage_buckets()
            
            # Fetch recommendations for cost savings
            try:
                recommendations = self.fetch_recommendations()
            except:
                recommendations = []
            
            # Calculate estimated costs (simplified)
            # In production, you'd get actual costs from BigQuery billing export
            estimated_compute_cost = len(instances) * 50 * (days / 30)  # $50/month per instance estimate
            estimated_storage_cost = len(buckets) * 20 * (days / 30)    # $20/month per bucket estimate
            
            summary = {
                "project_id": self.project_id,
                "analysis_period_days": days,
                "billing_enabled": billing_data.get("billing_enabled", False),
                "resource_counts": {
                    "compute_instances": len(instances),
                    "storage_buckets": len(buckets)
                },
                "estimated_costs": {
                    "compute": estimated_compute_cost,
                    "storage": estimated_storage_cost,
                    "total": estimated_compute_cost + estimated_storage_cost,
                    "note": "These are estimates. Enable BigQuery billing export for actual costs."
                },
                "optimization_potential": {
                    "recommendations_count": len(recommendations),
                    "estimated_savings": len(recommendations) * 25,  # Rough estimate
                    "note": "Based on available recommendations"
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Cost analysis summary generated")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate cost analysis summary: {e}")
            raise


# Export the class
__all__ = ['GCPClient']