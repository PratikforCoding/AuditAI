"""
GCP Cloud Billing API Service
UPDATED: Supports per-user credentials
Fetches real cost data from Cloud Billing export (BigQuery)
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)


class GCPBillingService:
    """Service to fetch actual costs from GCP Cloud Billing
    UPDATED: Supports per-user credentials"""
    
    def __init__(self, project_id: str, user_credentials: Optional[Dict] = None):
        """
        Initialize billing service
        
        Args:
            project_id: GCP Project ID
            user_credentials: Optional dict with user's service account JSON
        """
        self.project_id = project_id
        
        # Initialize BigQuery client with credentials
        if user_credentials:
            logger.info(f"🔑 Using user credentials for billing service: {project_id}")
            credentials = service_account.Credentials.from_service_account_info(
                user_credentials
            )
            self.bq_client = bigquery.Client(
                project=project_id, 
                credentials=credentials
            )
        else:
            logger.info(f"🔧 Using environment credentials for billing service: {project_id}")
            self.bq_client = bigquery.Client(project=project_id)
        
        # Make sure billing export is enabled in your GCP project
        # Settings → Billing → Billing export to BigQuery
        self.billing_dataset = "billing_export"  # Default dataset name
        
    def get_resource_cost(
        self,
        resource_id: str,
        resource_type: str,
        days: int = 30
    ) -> Dict[str, float]:
        """Get actual cost for a specific resource from past N days"""
        try:
            query = f"""
            SELECT
                DATE(DATE(TIMESTAMP_MICROS(usage_start_time))) as date,
                resource.name as resource_name,
                resource.type as resource_type,
                SUM(CAST(cost as FLOAT64)) as daily_cost,
                SUM(CAST(usage.amount as FLOAT64)) as usage_amount,
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_v1_*`
            WHERE
                DATE(TIMESTAMP_MICROS(usage_start_time)) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
                AND resource.name = '{resource_id}'
                AND resource.type = '{resource_type}'
            GROUP BY
                date,
                resource_name,
                resource_type
            ORDER BY
                date DESC
            """
            
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            rows = list(results)
            if not rows:
                logger.warning(f"No billing data found for {resource_id}")
                return {
                    'daily_average': 0.0,
                    'monthly_projection': 0.0,
                    'total_30_days': 0.0,
                    'currency': 'USD'
                }
            
            # Calculate statistics
            total_cost = sum(float(row['daily_cost']) for row in rows)
            daily_average = total_cost / len(rows) if rows else 0.0
            monthly_projection = daily_average * 30
            
            return {
                'daily_average': round(daily_average, 4),
                'monthly_projection': round(monthly_projection, 2),
                'total_30_days': round(total_cost, 2),
                'currency': 'USD',
                'data_points': len(rows)
            }
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching billing data: {e}")
            raise
            
    def get_project_total_cost(self, days: int = 30) -> Dict[str, any]:
        """Get total project cost for past N days"""
        try:
            query = f"""
            SELECT
                SUM(CAST(cost as FLOAT64)) as total_cost,
                COUNT(DISTINCT resource.name) as resource_count,
                COUNT(DISTINCT service.id) as service_count,
                ARRAY_AGG(DISTINCT service.description) as services
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_v1_*`
            WHERE
                DATE(TIMESTAMP_MICROS(usage_start_time)) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            """
            
            query_job = self.bq_client.query(query)
            result = list(query_job.result())[0]
            
            total_cost = float(result['total_cost']) if result['total_cost'] else 0.0
            
            return {
                'total_cost': round(total_cost, 2),
                'daily_average': round(total_cost / days, 2),
                'monthly_projection': round((total_cost / days) * 30, 2),
                'resource_count': result['resource_count'],
                'service_count': result['service_count'],
                'services': result['services'],
                'currency': 'USD',
                'period_days': days
            }
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching project cost: {e}")
            raise

    def get_cost_by_service(self, days: int = 30) -> List[Dict]:
        """Get cost breakdown by GCP service"""
        try:
            query = f"""
            SELECT
                service.description as service_name,
                service.id as service_id,
                SUM(CAST(cost as FLOAT64)) as total_cost,
                COUNT(DISTINCT resource.name) as resource_count
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_v1_*`
            WHERE
                DATE(TIMESTAMP_MICROS(usage_start_time)) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            GROUP BY
                service_name,
                service_id
            ORDER BY
                total_cost DESC
            """
            
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            return [
                {
                    'service_name': row['service_name'],
                    'service_id': row['service_id'],
                    'total_cost': round(float(row['total_cost']), 2),
                    'resource_count': row['resource_count']
                }
                for row in results
            ]
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching cost by service: {e}")
            raise

    def get_cost_trend(self, days: int = 90) -> List[Dict]:
        """Get daily cost trend for past N days"""
        try:
            query = f"""
            SELECT
                DATE(TIMESTAMP_MICROS(usage_start_time)) as date,
                SUM(CAST(cost as FLOAT64)) as daily_cost
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_v1_*`
            WHERE
                DATE(TIMESTAMP_MICROS(usage_start_time)) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            GROUP BY
                date
            ORDER BY
                date ASC
            """
            
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            return [
                {
                    'date': str(row['date']),
                    'cost': round(float(row['daily_cost']), 2)
                }
                for row in results
            ]
            
        except GoogleCloudError as e:
            logger.error(f"Error fetching cost trend: {e}")
            raise