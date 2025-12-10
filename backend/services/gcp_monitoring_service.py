"""
GCP Cloud Monitoring API Service
Fetches actual resource metrics (CPU, memory, disk usage)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from google.cloud import monitoring_v3
from google.cloud.exceptions import GoogleCloudError
import logging

logger = logging.getLogger(__name__)


class GCPMonitoringService:
    """Service to fetch real metrics from Cloud Monitoring"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        self.query_client = monitoring_v3.QueryServiceClient()
        self.project_name = f"projects/{project_id}"
        
    def get_compute_instance_metrics(
        self,
        instance_id: str,
        zone: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """
        Get CPU and memory metrics for a compute instance
        
        Args:
            instance_id: GCE instance ID
            zone: GCE zone
            hours: lookback period
            
        Returns:
            {
                'cpu_utilization_percent': float,
                'memory_utilization_percent': float,
                'is_idle': bool,
                'status': str,
                'last_updated': datetime
            }
        """
        try:
            # Query CPU utilization
            cpu_query = f"""
            fetch gce_instance
            | metric 'compute.googleapis.com/instance/cpu/utilization'
            | resource.instance_id == '{instance_id}'
            | resource.zone_id == '{zone}'
            | within {hours}h, d'1m'
            | mean_aligner()
            """
            
            cpu_results = self._execute_monitoring_query(cpu_query)
            cpu_avg = self._calculate_average_from_results(cpu_results)
            
            # Query memory utilization (if guest metrics enabled)
            memory_query = f"""
            fetch gce_instance
            | metric 'workload.googleapis.com/container/memory/usage'
            | resource.instance_id == '{instance_id}'
            | resource.zone_id == '{zone}'
            | within {hours}h, d'1m'
            | mean_aligner()
            """
            
            memory_results = self._execute_monitoring_query(memory_query)
            memory_avg = self._calculate_average_from_results(memory_results)
            
            # Determine if idle (industry standard: <5% CPU utilization for 24+ hours)
            is_idle = cpu_avg < 5.0
            
            return {
                'instance_id': instance_id,
                'zone': zone,
                'cpu_utilization_percent': round(cpu_avg, 2),
                'memory_utilization_percent': round(memory_avg, 2),
                'is_idle': is_idle,
                'lookback_hours': hours,
                'last_updated': datetime.utcnow().isoformat(),
                'idle_threshold_percent': 5.0
            }
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching instance metrics: {e}")
            raise
            
    def get_disk_utilization(
        self,
        disk_id: str,
        zone: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """Get disk usage metrics"""
        try:
            disk_query = f"""
            fetch gce_disk
            | metric 'compute.googleapis.com/disk/read_bytes_count'
            | resource.resource_id == '{disk_id}'
            | resource.zone_id == '{zone}'
            | within {hours}h, d'1h'
            | sum_aligner()
            """
            
            results = self._execute_monitoring_query(disk_query)
            total_read_bytes = sum(
                float(point['value']['double_value']) 
                for point in (results.get('points', []) or [])
            ) if results else 0.0
            
            # If no read activity in past 24 hours = unused
            is_unused = total_read_bytes == 0
            
            return {
                'disk_id': disk_id,
                'zone': zone,
                'total_read_bytes': total_read_bytes,
                'is_unused': is_unused,
                'lookback_hours': hours,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching disk metrics: {e}")
            raise
            
    def get_network_traffic(
        self,
        resource_id: str,
        resource_type: str,
        hours: int = 24
    ) -> Dict[str, any]:
        """Get network traffic (if any, resource is active)"""
        try:
            query = f"""
            fetch {resource_type}
            | metric 'compute.googleapis.com/instance/network/received_bytes_count'
            | resource.instance_id == '{resource_id}'
            | within {hours}h, d'1h'
            | sum_aligner()
            """
            
            results = self._execute_monitoring_query(query)
            total_bytes = sum(
                float(point['value']['double_value']) 
                for point in (results.get('points', []) or [])
            ) if results else 0.0
            
            return {
                'resource_id': resource_id,
                'total_received_bytes': total_bytes,
                'has_network_activity': total_bytes > 0,
                'lookback_hours': hours
            }
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching network metrics: {e}")
            raise
    
    def _execute_monitoring_query(self, query: str) -> Dict:
        """Execute MQL (Monitoring Query Language) query"""
        try:
            request = monitoring_v3.QueryTimeSeriesRequest(
                name=self.project_name,
                query=query
            )
            response = self.query_client.query_time_series(request=request)
            return response
        except GoogleCloudError as e:
            logger.error(f"Error executing monitoring query: {e}")
            raise
    
    def _calculate_average_from_results(self, results: Dict) -> float:
        """Calculate average value from monitoring query results"""
        try:
            if not results or not hasattr(results, 'time_series_data'):
                return 0.0
            
            values = []
            for point in results.time_series_data:
                if hasattr(point, 'values') and point.values:
                    for value in point.values:
                        if hasattr(value, 'double_value'):
                            values.append(value.double_value)
            
            return sum(values) / len(values) if values else 0.0
        except Exception as e:
            logger.error(f"Error calculating average: {e}")
            return 0.0
