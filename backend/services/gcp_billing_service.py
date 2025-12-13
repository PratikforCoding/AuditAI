"""
GCP Cloud Billing API Service - FIXED VERSION
Corrected BigQuery SQL queries and error handling
Supports per-user credentials
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)


class GCPBillingService:
    """
    Service to fetch actual costs from GCP Cloud Billing
    FIXED: Corrected BigQuery SQL syntax errors
    """
    
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
        
        # Billing export dataset name (configurable)
        # Default: "billing_export" but check your project's actual dataset name
        self.billing_dataset = os.getenv("BILLING_DATASET", "billing_export")
        
        logger.info(f"✅ Billing service initialized for project: {project_id}")
    
    def verify_billing_export(self) -> Dict[str, Any]:
        """
        Verify that billing export is enabled and find the correct table
        Returns table info if found, None otherwise
        """
        try:
            # List all datasets to find billing export
            datasets = list(self.bq_client.list_datasets())
            
            billing_datasets = []
            for dataset in datasets:
                dataset_id = dataset.dataset_id
                if 'billing' in dataset_id.lower():
                    billing_datasets.append(dataset_id)
                    
                    # Check for tables in this dataset
                    tables = list(self.bq_client.list_tables(f"{self.project_id}.{dataset_id}"))
                    table_names = [t.table_id for t in tables]
                    
                    if table_names:
                        logger.info(f"✅ Found billing dataset: {dataset_id} with {len(table_names)} tables")
                        return {
                            "has_billing_export": True,
                            "dataset_id": dataset_id,
                            "tables": table_names,
                            "table_count": len(table_names)
                        }
            
            logger.warning(f"⚠️ No billing export tables found. Available datasets: {[d.dataset_id for d in datasets]}")
            return {
                "has_billing_export": False,
                "available_datasets": [d.dataset_id for d in datasets],
                "message": "Billing export not configured. Enable at: GCP Console → Billing → Billing Export"
            }
            
        except Exception as e:
            logger.error(f"❌ Error verifying billing export: {e}")
            return {
                "has_billing_export": False,
                "error": str(e)
            }
    
    def get_project_total_cost(self, days: int = 30) -> Dict[str, any]:
        """
        Get total project cost for past N days
        FIXED: Corrected SQL syntax - removed 'resource' reference
        """
        try:
            # ✅ FIXED: Use correct column names without 'resource' alias
            query = f"""
            SELECT
                SUM(CAST(cost AS FLOAT64)) as total_cost,
                SUM((SELECT SUM(CAST(c.amount AS FLOAT64)) FROM UNNEST(credits) AS c)) as total_credits,
                COUNT(DISTINCT service.description) as service_count,
                ARRAY_AGG(DISTINCT service.description IGNORE NULLS LIMIT 100) as services
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_resource_v1_*`
            WHERE
                _TABLE_SUFFIX BETWEEN 
                    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY))
                    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
                AND cost > 0
            """
            
            logger.info(f"Executing billing query for {days} days...")
            query_job = self.bq_client.query(query)
            result = list(query_job.result())
            
            if not result or len(result) == 0:
                logger.warning("No billing data found - returning zero costs")
                return self._get_empty_cost_response(days)
            
            row = result[0]
            total_cost = float(row['total_cost']) if row['total_cost'] else 0.0
            total_credits = float(row['total_credits']) if row.get('total_credits') else 0.0
            net_cost = total_cost - abs(total_credits)
            
            logger.info(f"✅ Total cost (last {days} days): ${total_cost:.2f}")
            
            return {
                'total_cost': round(total_cost, 2),
                'total_credits': round(abs(total_credits), 2),
                'net_cost': round(net_cost, 2),
                'daily_average': round(total_cost / days, 2),
                'monthly_projection': round((total_cost / days) * 30, 2),
                'service_count': row['service_count'] or 0,
                'services': row['services'] or [],
                'currency': 'USD',
                'period_days': days,
                'data_available': True
            }
            
        except GoogleCloudError as e:
            logger.error(f"❌ Error fetching project cost: {e}")
            
            # Check if billing export is configured
            if "not found" in str(e).lower() or "does not exist" in str(e).lower():
                logger.warning("⚠️ Billing export table not found. Returning zero costs.")
                return self._get_empty_cost_response(days, error="Billing export not configured")
            
            raise
    
    def get_cost_by_service(self, days: int = 30) -> List[Dict]:
        """
        Get cost breakdown by GCP service
        FIXED: Removed invalid 'resource' reference
        """
        try:
            # ✅ FIXED: Corrected query without resource reference
            query = f"""
            SELECT
                service.description as service_name,
                service.id as service_id,
                SUM(CAST(cost AS FLOAT64)) as total_cost,
                SUM(CAST(usage.amount AS FLOAT64)) as usage_amount
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_resource_v1_*`
            WHERE
                _TABLE_SUFFIX BETWEEN 
                    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY))
                    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
                AND cost > 0
            GROUP BY
                service_name,
                service_id
            ORDER BY
                total_cost DESC
            LIMIT 20
            """
            
            logger.info(f"Fetching cost by service for {days} days...")
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            services = [
                {
                    'service_name': row['service_name'],
                    'service_id': row['service_id'],
                    'total_cost': round(float(row['total_cost']), 2),
                    'usage_amount': round(float(row.get('usage_amount', 0)), 2) if row.get('usage_amount') else 0
                }
                for row in results
            ]
            
            logger.info(f"✅ Found {len(services)} services with costs")
            return services
            
        except GoogleCloudError as e:
            logger.error(f"❌ Error fetching cost by service: {e}")
            
            if "not found" in str(e).lower():
                logger.warning("⚠️ Billing export not found. Returning empty list.")
                return []
            
            raise

    def get_cost_trend(self, days: int = 90) -> List[Dict]:
        """
        Get daily cost trend for past N days
        FIXED: Uses correct date column
        """
        try:
            query = f"""
            SELECT
                DATE(usage_start_time) as date,
                SUM(CAST(cost AS FLOAT64)) as daily_cost
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_resource_v1_*`
            WHERE
                _TABLE_SUFFIX BETWEEN 
                    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY))
                    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
                AND cost > 0
            GROUP BY
                date
            ORDER BY
                date ASC
            """
            
            logger.info(f"Fetching cost trend for {days} days...")
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            trend = [
                {
                    'date': str(row['date']),
                    'cost': round(float(row['daily_cost']), 2)
                }
                for row in results
            ]
            
            logger.info(f"✅ Cost trend fetched: {len(trend)} data points")
            return trend
            
        except GoogleCloudError as e:
            logger.error(f"❌ Error fetching cost trend: {e}")
            
            if "not found" in str(e).lower():
                return []
            
            raise
    
    def get_resource_cost(
        self,
        resource_name: str,
        days: int = 30
    ) -> Dict[str, float]:
        """
        Get actual cost for a specific resource from past N days
        FIXED: Uses correct column references
        """
        try:
            query = f"""
            SELECT
                DATE(usage_start_time) as date,
                SUM(CAST(cost AS FLOAT64)) as daily_cost
            FROM
                `{self.project_id}.{self.billing_dataset}.gcp_billing_export_resource_v1_*`
            WHERE
                _TABLE_SUFFIX BETWEEN 
                    FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY))
                    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
                AND LOWER(resource.name) LIKE LOWER('%{resource_name}%')
                AND cost > 0
            GROUP BY
                date
            ORDER BY
                date DESC
            """
            
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            rows = list(results)
            if not rows:
                logger.warning(f"No billing data found for resource: {resource_name}")
                return {
                    'daily_average': 0.0,
                    'monthly_projection': 0.0,
                    'total_cost': 0.0,
                    'currency': 'USD',
                    'data_points': 0
                }
            
            # Calculate statistics
            total_cost = sum(float(row['daily_cost']) for row in rows)
            daily_average = total_cost / len(rows) if rows else 0.0
            monthly_projection = daily_average * 30
            
            return {
                'daily_average': round(daily_average, 4),
                'monthly_projection': round(monthly_projection, 2),
                'total_cost': round(total_cost, 2),
                'currency': 'USD',
                'data_points': len(rows)
            }
            
        except GoogleCloudError as e:
            logger.error(f"❌ Error fetching resource cost: {e}")
            raise
    
    def _get_empty_cost_response(self, days: int, error: str = None) -> Dict[str, any]:
        """Return empty cost response when no data is available"""
        response = {
            'total_cost': 0.0,
            'total_credits': 0.0,
            'net_cost': 0.0,
            'daily_average': 0.0,
            'monthly_projection': 0.0,
            'service_count': 0,
            'services': [],
            'currency': 'USD',
            'period_days': days,
            'data_available': False
        }
        
        if error:
            response['message'] = error
            response['setup_instructions'] = (
                "To enable billing export: "
                "1. Go to GCP Console → Billing → Billing Export "
                "2. Enable 'Daily cost detail' export to BigQuery "
                "3. Wait 24 hours for data to populate"
            )
        
        return response


# Usage example and testing
if __name__ == "__main__":
    import sys
    
    project_id = os.getenv("GOOGLE_PROJECT_ID", "test-project")
    
    try:
        service = GCPBillingService(project_id)
        
        # First, verify billing export is configured
        billing_status = service.verify_billing_export()
        print(f"📊 Billing Export Status:")
        print(json.dumps(billing_status, indent=2))
        
        if billing_status.get('has_billing_export'):
            # Get cost data
            costs = service.get_project_total_cost(days=30)
            print(f"\n💰 Project Costs (last 30 days):")
            print(json.dumps(costs, indent=2))
            
            # Get cost by service
            by_service = service.get_cost_by_service(days=30)
            print(f"\n📈 Cost by Service:")
            for svc in by_service[:5]:  # Top 5
                print(f"  - {svc['service_name']}: ${svc['total_cost']}")
        else:
            print("\n⚠️ Billing export not configured. Enable it to see cost data.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)