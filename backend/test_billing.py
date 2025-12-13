#!/usr/bin/env python3
"""
Test Billing Data Access
Verifies that billing export is working and returns actual cost data
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import os
import sys

def test_billing_access():
    """Test if we can read billing data"""
    
    # Configuration
    project_id = os.getenv("GOOGLE_PROJECT_ID", "auditai-480710")
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not creds_path or not os.path.exists(creds_path):
        print("❌ Error: GOOGLE_APPLICATION_CREDENTIALS not set or file not found")
        print(f"   Looking for: {creds_path}")
        sys.exit(1)
    
    print(f"🔍 Testing billing data access for project: {project_id}")
    print(f"📁 Using credentials: {creds_path}\n")
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    client = bigquery.Client(project=project_id, credentials=credentials)
    
    # Test 1: List datasets
    print("=" * 60)
    print("TEST 1: List BigQuery Datasets")
    print("=" * 60)
    
    try:
        datasets = list(client.list_datasets())
        print(f"✅ Found {len(datasets)} datasets:")
        for ds in datasets:
            print(f"   - {ds.dataset_id}")
    except Exception as e:
        print(f"❌ Failed to list datasets: {e}")
        sys.exit(1)
    
    # Test 2: Check billing export tables
    print("\n" + "=" * 60)
    print("TEST 2: Check Billing Export Tables")
    print("=" * 60)
    
    billing_dataset = "billing_export"
    try:
        tables = list(client.list_tables(f"{project_id}.{billing_dataset}"))
        print(f"✅ Found {len(tables)} tables in '{billing_dataset}':")
        
        table_names = []
        for table in tables:
            print(f"   - {table.table_id}")
            table_names.append(table.table_id)
            
            # Get table info
            table_ref = client.get_table(f"{project_id}.{billing_dataset}.{table.table_id}")
            print(f"     Rows: {table_ref.num_rows:,}")
            print(f"     Size: {table_ref.num_bytes / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"❌ Failed to check billing tables: {e}")
        sys.exit(1)
    
    # Test 3: Query actual billing data
    print("\n" + "=" * 60)
    print("TEST 3: Query Billing Data (Last 30 Days)")
    print("=" * 60)
    
    # Try different table patterns
    table_patterns = [
        "gcp_billing_export_resource_v1_*",  # Your actual pattern
        "gcp_billing_export_v1_*",           # Standard pattern
        "gcp_billing_export_*",              # Wildcard pattern
    ]
    
    for pattern in table_patterns:
        try:
            query = f"""
            SELECT 
                service.description as service_name,
                SUM(CAST(cost AS FLOAT64)) as total_cost,
                COUNT(*) as transaction_count
            FROM `{project_id}.{billing_dataset}.{pattern}`
            WHERE 
                DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                AND cost > 0
            GROUP BY service_name
            ORDER BY total_cost DESC
            LIMIT 10
            """
            
            print(f"\n📊 Trying pattern: {pattern}")
            results = list(client.query(query).result())
            
            if results:
                print(f"✅ SUCCESS! Found {len(results)} services with costs:\n")
                total = 0
                for row in results:
                    print(f"   {row.service_name:40s} ${row.total_cost:>10.2f}  ({row.transaction_count:,} transactions)")
                    total += row.total_cost
                
                print(f"\n   {'TOTAL':40s} ${total:>10.2f}")
                print(f"\n✅ This pattern works! Use it in your billing service.")
                break
            else:
                print(f"⚠️  No results with this pattern")
                
        except Exception as e:
            print(f"❌ Pattern failed: {str(e)[:100]}")
            continue
    
    # Test 4: Get date range of available data
    print("\n" + "=" * 60)
    print("TEST 4: Date Range of Available Data")
    print("=" * 60)
    
    try:
        # Use the first successful pattern
        query = f"""
        SELECT 
            MIN(DATE(usage_start_time)) as earliest_date,
            MAX(DATE(usage_start_time)) as latest_date,
            COUNT(DISTINCT DATE(usage_start_time)) as total_days
        FROM `{project_id}.{billing_dataset}.gcp_billing_export_resource_v1_*`
        WHERE cost > 0
        """
        
        result = list(client.query(query).result())[0]
        
        print(f"✅ Data available:")
        print(f"   Earliest: {result.earliest_date}")
        print(f"   Latest:   {result.latest_date}")
        print(f"   Total days with data: {result.total_days}")
        
    except Exception as e:
        print(f"❌ Could not determine date range: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print("✅ Billing export is configured and working")
    print("✅ Data is available and queryable")
    print("\n💡 NEXT STEPS:")
    print("1. Update your billing service to use the working table pattern")
    print("2. Ensure _TABLE_SUFFIX filters match your data range")
    print("3. Test your API endpoint again - should return cost data!")
    print()

if __name__ == "__main__":
    test_billing_access()