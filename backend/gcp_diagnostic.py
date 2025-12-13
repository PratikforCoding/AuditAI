"""
GCP Data Collection Diagnostic Tool
Checks why your analysis is returning empty data
Run this to identify configuration issues
"""

import os
import sys
import json
from google.cloud import bigquery, compute_v1, monitoring_v3
from google.oauth2 import service_account
from google.cloud import recommender_v1

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(status, message):
    """Print colored status message"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_billing_export(project_id, credentials):
    """Check if billing export is configured"""
    print("\n" + "="*60)
    print("1. CHECKING BILLING EXPORT (BigQuery)")
    print("="*60)
    
    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
        
        # List all datasets
        datasets = list(client.list_datasets())
        dataset_ids = [d.dataset_id for d in datasets]
        
        print_status("info", f"Found {len(datasets)} datasets in project")
        
        # Look for billing datasets
        billing_datasets = [d for d in dataset_ids if 'billing' in d.lower()]
        
        if billing_datasets:
            print_status("success", f"Found billing datasets: {billing_datasets}")
            
            # Check for tables in billing datasets
            for dataset_id in billing_datasets:
                tables = list(client.list_tables(f"{project_id}.{dataset_id}"))
                table_names = [t.table_id for t in tables]
                
                if table_names:
                    print_status("success", f"Dataset '{dataset_id}' has {len(table_names)} tables")
                    
                    # Try to query for data
                    for table_name in table_names[:1]:  # Check first table
                        query = f"""
                        SELECT COUNT(*) as row_count
                        FROM `{project_id}.{dataset_id}.{table_name}`
                        LIMIT 1
                        """
                        try:
                            result = list(client.query(query).result())[0]
                            row_count = result['row_count']
                            if row_count > 0:
                                print_status("success", f"Table '{table_name}' has {row_count} rows of billing data")
                            else:
                                print_status("warning", f"Table '{table_name}' exists but has no data yet")
                        except Exception as e:
                            print_status("error", f"Could not query table: {str(e)}")
                else:
                    print_status("warning", f"Dataset '{dataset_id}' has no tables")
        else:
            print_status("error", "No billing datasets found")
            print("\n📋 TO FIX:")
            print("1. Go to: https://console.cloud.google.com/billing")
            print("2. Select your billing account")
            print("3. Click 'Billing export'")
            print("4. Enable 'Daily cost detail' export to BigQuery")
            print("5. Wait 24 hours for data to populate")
            
    except Exception as e:
        print_status("error", f"Billing check failed: {str(e)}")

def check_compute_resources(project_id, credentials):
    """Check if there are any compute resources"""
    print("\n" + "="*60)
    print("2. CHECKING COMPUTE ENGINE RESOURCES")
    print("="*60)
    
    try:
        client = compute_v1.InstancesClient(credentials=credentials)
        
        # List zones
        zones_client = compute_v1.ZonesClient(credentials=credentials)
        zones_request = compute_v1.ListZonesRequest(project=project_id)
        zones = list(zones_client.list(request=zones_request))
        
        total_instances = 0
        
        # Check a few common zones
        common_zones = ['us-central1-a', 'us-east1-b', 'europe-west1-b', 'asia-south1-a']
        zones_to_check = [z.name for z in zones if z.name in common_zones][:5]
        
        if not zones_to_check:
            zones_to_check = [z.name for z in zones[:5]]
        
        for zone_name in zones_to_check:
            try:
                request = compute_v1.ListInstancesRequest(
                    project=project_id,
                    zone=zone_name
                )
                instances = list(client.list(request=request))
                
                if instances:
                    total_instances += len(instances)
                    print_status("success", f"Zone '{zone_name}': {len(instances)} instances")
                    for instance in instances[:3]:  # Show first 3
                        print(f"    - {instance.name} ({instance.status})")
            except Exception as e:
                if "404" not in str(e):
                    print_status("warning", f"Could not check zone '{zone_name}': {str(e)}")
        
        if total_instances == 0:
            print_status("warning", "No compute instances found in any zone")
            print("\n📋 NOTE: This is OK if:")
            print("- You're not using Compute Engine")
            print("- Your instances are in different zones")
            print("- You're using Cloud Run, Cloud Functions, or GKE instead")
        else:
            print_status("success", f"Total: {total_instances} compute instances found")
            
    except Exception as e:
        print_status("error", f"Compute check failed: {str(e)}")

def check_monitoring_access(project_id, credentials):
    """Check if monitoring API is accessible"""
    print("\n" + "="*60)
    print("3. CHECKING CLOUD MONITORING ACCESS")
    print("="*60)
    
    try:
        client = monitoring_v3.QueryServiceClient(credentials=credentials)
        project_name = f"projects/{project_id}"
        
        # Simple test query
        query = """
        fetch gce_instance
        | metric 'compute.googleapis.com/instance/cpu/utilization'
        | within 1h
        | group_by [], [value_count: count(value.double_value)]
        """
        
        request = monitoring_v3.QueryTimeSeriesRequest(
            name=project_name,
            query=query
        )
        
        response = client.query_time_series(request=request)
        print_status("success", "Cloud Monitoring API is accessible")
        
        # Check if there's any data
        has_data = False
        if hasattr(response, 'time_series_data'):
            has_data = len(list(response.time_series_data)) > 0
        
        if has_data:
            print_status("success", "Found monitoring data for compute instances")
        else:
            print_status("warning", "No monitoring data found (this is OK if no VMs exist)")
            
    except Exception as e:
        print_status("error", f"Monitoring check failed: {str(e)}")
        print("\n📋 TO FIX:")
        print("1. Enable Cloud Monitoring API")
        print("2. Grant 'roles/monitoring.viewer' to service account")

def check_recommender_access(project_id, credentials):
    """Check if recommender API is accessible"""
    print("\n" + "="*60)
    print("4. CHECKING RECOMMENDER API ACCESS")
    print("="*60)
    
    try:
        client = recommender_v1.RecommenderClient(credentials=credentials)
        
        # Check idle VM recommender
        recommender_name = f"projects/{project_id}/locations/global/recommenders/google.compute.instance.IdleResourceRecommender"
        
        try:
            request = recommender_v1.ListRecommendationsRequest(
                parent=recommender_name,
                page_size=10
            )
            recommendations = list(client.list_recommendations(request=request))
            
            if recommendations:
                print_status("success", f"Found {len(recommendations)} recommendations")
                for rec in recommendations[:3]:
                    print(f"    - {rec.description[:80]}...")
            else:
                print_status("warning", "No recommendations found (this is good - no idle resources!)")
                
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                print_status("warning", "Recommender not available for this project")
            else:
                print_status("error", f"Recommender check failed: {str(e)}")
                
    except Exception as e:
        print_status("error", f"Recommender API check failed: {str(e)}")
        print("\n📋 TO FIX:")
        print("1. Enable Recommender API")
        print("2. Grant 'roles/recommender.viewer' to service account")

def check_service_account_permissions(project_id, credentials):
    """Check service account permissions"""
    print("\n" + "="*60)
    print("5. CHECKING SERVICE ACCOUNT PERMISSIONS")
    print("="*60)
    
    try:
        # Get service account email from credentials
        if hasattr(credentials, 'service_account_email'):
            email = credentials.service_account_email
            print_status("info", f"Service Account: {email}")
        else:
            print_status("info", "Service Account: (email not available)")
        
        print("\n📋 REQUIRED ROLES:")
        required_roles = [
            ("roles/viewer", "Read all resources"),
            ("roles/billing.viewer", "Read billing data"),
            ("roles/monitoring.viewer", "Read metrics"),
            ("roles/recommender.viewer", "Read recommendations"),
            ("roles/bigquery.dataViewer", "Read BigQuery data")
        ]
        
        for role, description in required_roles:
            print(f"  • {role} - {description}")
        
        print("\n💡 TO VERIFY PERMISSIONS:")
        print("1. Go to: https://console.cloud.google.com/iam-admin/iam")
        print("2. Find your service account")
        print("3. Check it has the roles listed above")
        
    except Exception as e:
        print_status("error", f"Permission check failed: {str(e)}")

def main():
    """Run all diagnostic checks"""
    print("\n" + "="*60)
    print("🔍 GCP DATA COLLECTION DIAGNOSTICS")
    print("="*60)
    
    # Get project ID and credentials
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not project_id:
        print_status("error", "GOOGLE_PROJECT_ID not set")
        print("Set it with: export GOOGLE_PROJECT_ID=your-project-id")
        sys.exit(1)
    
    print_status("info", f"Project ID: {project_id}")
    
    # Load credentials
    if credentials_path and os.path.exists(credentials_path):
        print_status("info", f"Credentials: {credentials_path}")
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    else:
        print_status("error", "GOOGLE_APPLICATION_CREDENTIALS not set or file not found")
        print("Set it with: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json")
        sys.exit(1)
    
    # Run all checks
    check_billing_export(project_id, credentials)
    check_compute_resources(project_id, credentials)
    check_monitoring_access(project_id, credentials)
    check_recommender_access(project_id, credentials)
    check_service_account_permissions(project_id, credentials)
    
    # Summary
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*60)
    print("\nIf all checks show ✅, your configuration is correct.")
    print("If you see ❌ or ⚠️, follow the instructions above each section.")
    print("\n💡 MOST COMMON ISSUES:")
    print("1. Billing export not enabled → No cost data")
    print("2. No compute resources → No metrics data")
    print("3. Missing IAM roles → API access denied")
    print("4. Service account in wrong project → Can't see resources")
    print("\n")

if __name__ == "__main__":
    main()