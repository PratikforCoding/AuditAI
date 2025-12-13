"""
GCP Cloud Monitoring API Service - FIXED VERSION
Corrected MQL (Monitoring Query Language) syntax
Supports per-user credentials
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from google.cloud import monitoring_v3
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)


class GCPMonitoringService:
    """
    Service to fetch real metrics from Cloud Monitoring
    FIXED: Corrected MQL queries with proper field names
    """
    
    def __init__(self, project_id: str, user_credentials: Optional[Dict] = None):
        """
        Initialize monitoring service
        
        Args:
            project_id: GCP Project ID
            user_credentials: Optional dict with user's service account JSON
        """
        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        
        try:
            # Initialize monitoring clients with credentials
            if user_credentials:
                logger.info(f"🔒 Using user credentials for monitoring service: {project_id}")
                
                credentials = service_account.Credentials.from_service_account_info(
                    user_credentials,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                
                self.client = monitoring_v3.MetricServiceClient(credentials=credentials)
                self.query_client = monitoring_v3.QueryServiceClient(credentials=credentials)
            else:
                logger.info(f"🔧 Using environment credentials for monitoring service: {project_id}")
                
                self.client = monitoring_v3.MetricServiceClient()
                self.query_client = monitoring_v3.QueryServiceClient()
            
            logger.info(f"✅ Monitoring service initialized for project: {project_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize monitoring service: {e}")
            raise
    
    def get_compute_instance_metrics(
        self,
        instance_id: str,
        zone: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """
        Get CPU and memory metrics for a compute instance
        FIXED: Uses correct metric names and field references
        """
        try:
            # ✅ FIXED: Use mean(value) for CPU metric (not value.double_value)
            cpu_query = f"""
            fetch gce_instance
            | metric 'compute.googleapis.com/instance/cpu/utilization'
            | filter resource.instance_id == '{instance_id}'
            | filter resource.zone == '{zone}'
            | within {hours}h
            | group_by [], [value_cpu_mean: mean(value)]
            """
            
            cpu_results = self._execute_monitoring_query(cpu_query)
            cpu_avg = self._extract_single_value(cpu_results)
            
            # Convert to percentage (metric returns 0-1 range)
            cpu_percent = cpu_avg * 100 if cpu_avg else 0.0
            
            # Determine if idle (industry standard: <5% CPU utilization for 24+ hours)
            is_idle = cpu_percent < 5.0
            
            logger.info(f"Instance {instance_id}: CPU={cpu_percent:.2f}%, Idle={is_idle}")
            
            return {
                'instance_id': instance_id,
                'zone': zone,
                'cpu_utilization_percent': round(cpu_percent, 2),
                'memory_utilization_percent': 0.0,  # Requires guest agent
                'is_idle': is_idle,
                'lookback_hours': hours,
                'last_updated': datetime.utcnow().isoformat(),
                'idle_threshold_percent': 5.0,
                'note': 'Memory metrics require Cloud Monitoring agent installation'
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching instance metrics for {instance_id}: {e}")
            # Return safe defaults
            return {
                'instance_id': instance_id,
                'zone': zone,
                'cpu_utilization_percent': 0.0,
                'memory_utilization_percent': 0.0,
                'is_idle': False,
                'lookback_hours': hours,
                'error': str(e),
                'data_available': False
            }
    
    def get_all_instances_metrics(self, hours: int = 24) -> List[Dict]:
        """
        Get metrics for all compute instances in the project
        FIXED: Corrected MQL query syntax
        """
        try:
            # ✅ FIXED: Use mean(value) for CPU metric
            query = f"""
            fetch gce_instance
            | metric 'compute.googleapis.com/instance/cpu/utilization'
            | within {hours}h
            | group_by [resource.instance_id, resource.zone],
                [value_cpu_mean: mean(value)]
            """
            
            logger.info("Fetching metrics for all instances...")
            results = self._execute_monitoring_query(query)
            
            instances_metrics = []
            
            if hasattr(results, 'time_series_data'):
                for ts_data in results.time_series_data:
                    try:
                        # Extract instance_id and zone from labels
                        instance_id = None
                        zone = None
                        
                        if hasattr(ts_data, 'label_values') and ts_data.label_values:
                            for i, label_value in enumerate(ts_data.label_values):
                                if hasattr(label_value, 'string_value'):
                                    if i == 0:
                                        instance_id = label_value.string_value
                                    elif i == 1:
                                        zone = label_value.string_value
                        
                        # Extract CPU value
                        cpu_value = 0.0
                        if hasattr(ts_data, 'point_data') and ts_data.point_data:
                            values = []
                            for point in ts_data.point_data:
                                if hasattr(point, 'values') and point.values:
                                    for val in point.values:
                                        if hasattr(val, 'double_value'):
                                            values.append(val.double_value)
                            
                            if values:
                                cpu_value = sum(values) / len(values)
                        
                        if instance_id:
                            cpu_percent = cpu_value * 100
                            instances_metrics.append({
                                'instance_id': instance_id,
                                'zone': zone or 'unknown',
                                'cpu_utilization_percent': round(cpu_percent, 2),
                                'is_idle': cpu_percent < 5.0,
                                'lookback_hours': hours
                            })
                    
                    except Exception as e:
                        logger.warning(f"Error parsing instance data: {e}")
                        continue
            
            logger.info(f"✅ Fetched metrics for {len(instances_metrics)} instances")
            return instances_metrics
            
        except Exception as e:
            logger.error(f"❌ Error fetching all instances metrics: {e}")
            return []
    
    def get_disk_utilization(
        self,
        disk_id: str,
        zone: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """
        Get disk usage metrics
        FIXED: Uses correct disk metric
        """
        try:
            # ✅ FIXED: Proper disk read operations query
            query = f"""
            fetch gce_disk
            | metric 'compute.googleapis.com/instance/disk/read_bytes_count'
            | filter resource.disk_name == '{disk_id}'
            | filter resource.zone == '{zone}'
            | within {hours}h
            | group_by [], [value_read_total: sum(value.int64_value)]
            """
            
            results = self._execute_monitoring_query(query)
            total_read_bytes = self._extract_single_value(results) or 0.0
            
            # If no read activity in past 24 hours = potentially unused
            is_unused = total_read_bytes == 0
            
            return {
                'disk_id': disk_id,
                'zone': zone,
                'total_read_bytes': total_read_bytes,
                'is_unused': is_unused,
                'lookback_hours': hours,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching disk metrics: {e}")
            return {
                'disk_id': disk_id,
                'zone': zone,
                'total_read_bytes': 0.0,
                'is_unused': False,
                'error': str(e),
                'data_available': False
            }
    
    def get_network_traffic(
        self,
        instance_id: str,
        zone: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """
        Get network traffic (if any, resource is active)
        FIXED: Correct network metric query
        """
        try:
            query = f"""
            fetch gce_instance
            | metric 'compute.googleapis.com/instance/network/received_bytes_count'
            | filter resource.instance_id == '{instance_id}'
            | filter resource.zone == '{zone}'
            | within {hours}h
            | group_by [], [value_bytes_total: sum(value.int64_value)]
            """
            
            results = self._execute_monitoring_query(query)
            total_bytes = self._extract_single_value(results) or 0.0
            
            return {
                'instance_id': instance_id,
                'zone': zone,
                'total_received_bytes': total_bytes,
                'has_network_activity': total_bytes > 0,
                'lookback_hours': hours
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching network metrics: {e}")
            return {
                'instance_id': instance_id,
                'zone': zone,
                'total_received_bytes': 0.0,
                'has_network_activity': False,
                'error': str(e)
            }
    
    def _execute_monitoring_query(self, query: str):
        """
        Execute MQL (Monitoring Query Language) query
        FIXED: Better error handling
        """
        try:
            request = monitoring_v3.QueryTimeSeriesRequest(
                name=self.project_name,
                query=query
            )
            response = self.query_client.query_time_series(request=request)
            return response
            
        except GoogleCloudError as e:
            logger.error(f"❌ Error executing monitoring query: {e}")
            logger.debug(f"Query was: {query}")
            raise
    
    def _extract_single_value(self, results) -> float:
        """
        Extract a single aggregated value from query results
        Helper for mean, sum, etc. queries
        """
        try:
            if not results or not hasattr(results, 'time_series_data'):
                return 0.0
            
            for ts_data in results.time_series_data:
                if hasattr(ts_data, 'point_data') and ts_data.point_data:
                    for point in ts_data.point_data:
                        if hasattr(point, 'values') and point.values:
                            for value in point.values:
                                if hasattr(value, 'double_value'):
                                    return value.double_value
                                elif hasattr(value, 'int64_value'):
                                    return float(value.int64_value)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"❌ Error extracting value: {e}")
            return 0.0
    
    def verify_monitoring_access(self) -> bool:
        """
        Verify that monitoring API is accessible
        Returns True if we can query metrics
        """
        try:
            # Simple test query - use count(value) not count(value.double_value)
            query = f"""
            fetch gce_instance
            | metric 'compute.googleapis.com/instance/cpu/utilization'
            | within 1h
            | group_by [], [value_count: count(value)]
            """
            
            request = monitoring_v3.QueryTimeSeriesRequest(
                name=self.project_name,
                query=query
            )
            self.query_client.query_time_series(request=request)
            
            logger.info("✅ Monitoring API access verified")
            return True
            
        except Exception as e:
            logger.error(f"❌ Monitoring API access verification failed: {e}")
            return False


# Usage example
if __name__ == "__main__":
    import os
    import json
    
    project_id = os.getenv("GOOGLE_PROJECT_ID", "test-project")
    
    try:
        service = GCPMonitoringService(project_id)
        
        if service.verify_monitoring_access():
            print("✅ Monitoring service is ready!")
            
            # Get metrics for all instances
            metrics = service.get_all_instances_metrics(hours=24)
            print(f"\n📊 Instance Metrics (last 24h):")
            print(json.dumps(metrics, indent=2))
        else:
            print("❌ Monitoring service verification failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")