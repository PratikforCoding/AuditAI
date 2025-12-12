"""
GCP Client - Google Cloud Platform Resource Manager
Handles authentication and API interactions with GCP services
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from google.cloud import compute_v1, storage_v1, monitoring_v3, billing_v1
from google.oauth2 import service_account
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GCPClient:
    """
    Client for interacting with Google Cloud Platform services
    Manages credentials and provides methods for fetching GCP resources
    """

    def __init__(self, project_id: str):
        """
        Initialize GCP Client with project credentials
        
        Args:
            project_id: GCP Project ID
        """
        self.project_id = project_id
        
        try:
            # Initialize GCP clients for different services
            self.compute_client = compute_v1.InstancesClient()
            self.storage_client = storage_v1.Client()
            self.monitoring_client = monitoring_v3.MetricServiceClient()
            self.billing_client = billing_v1.CloudBillingClient()
            
            logger.info(f"GCP Client initialized for project: {project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize GCP Client: {str(e)}")
            raise

    def fetch_compute_instances(self, zone: str = "us-central1-a") -> List[Dict[str, Any]]:
        """
        Fetch all Compute Engine instances in a specific zone
        
        Args:
            zone: GCP zone (default: us-central1-a)
        
        Returns:
            List of instance details
        """
        try:
            request = compute_v1.ListInstancesRequest(
                project=self.project_id,
                zone=zone,
            )
            
            instances = []
            page_result = self.compute_client.list(request=request)
            
            for instance in page_result:
                instances.append({
                    "name": instance.name,
                    "status": instance.status,
                    "machine_type": instance.machine_type,
                    "creation_timestamp": instance.creation_timestamp,
                    "cpu_platform": instance.cpu_platform,
                    "zone": zone,
                })
            
            logger.info(f"Fetched {len(instances)} instances from zone {zone}")
            return instances
        
        except Exception as e:
            logger.error(f"Failed to fetch compute instances: {str(e)}")
            return []

    def fetch_storage_buckets(self) -> List[Dict[str, Any]]:
        """
        Fetch all Cloud Storage buckets in the project
        
        Returns:
            List of bucket details
        """
        try:
            buckets = []
            
            for bucket in self.storage_client.list_buckets(project=self.project_id):
                buckets.append({
                    "name": bucket.name,
                    "created": str(bucket.time_created),
                    "location": bucket.location,
                    "storage_class": bucket.storage_class,
                })
            
            logger.info(f"Fetched {len(buckets)} storage buckets")
            return buckets
        
        except Exception as e:
            logger.error(f"Failed to fetch storage buckets: {str(e)}")
            return []

    def fetch_project_info(self) -> Dict[str, Any]:
        """
        Fetch basic project information
        
        Returns:
            Project details
        """
        try:
            return {
                "project_id": self.project_id,
                "status": "active",
            }
        except Exception as e:
            logger.error(f"Failed to fetch project info: {str(e)}")
            return {}

    def verify_credentials(self) -> bool:
        """
        Verify that GCP credentials are properly configured
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Try to fetch project info as a simple test
            self.fetch_project_info()
            logger.info("GCP credentials verified successfully")
            return True
        except Exception as e:
            logger.error(f"GCP credentials verification failed: {str(e)}")
            return False

    def get_resource_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all resources in the project
        
        Returns:
            Summary of resources
        """
        try:
            return {
                "project_id": self.project_id,
                "instances": len(self.fetch_compute_instances()),
                "buckets": len(self.fetch_storage_buckets()),
            }
        except Exception as e:
            logger.error(f"Failed to get resource summary: {str(e)}")
            return {"error": str(e)}


# For testing
if __name__ == "__main__":
    import sys
    
    project_id = os.getenv("GOOGLE_PROJECT_ID", "test-project")
    
    try:
        client = GCPClient(project_id)
        
        if client.verify_credentials():
            print("✅ GCP Client is ready!")
            summary = client.get_resource_summary()
            print(f"Project Summary: {summary}")
        else:
            print("❌ GCP credentials verification failed")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)