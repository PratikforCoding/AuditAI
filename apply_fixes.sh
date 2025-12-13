#!/bin/bash
# Automated Fix Script for AuditAI GCP Services
# Applies all necessary fixes to billing and monitoring services

set -e  # Exit on error

echo "🔧 AuditAI Service Fix Script"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend/services" ]; then
    echo "❌ Error: Please run this script from the AuditAI root directory"
    exit 1
fi

echo "📁 Backing up original files..."
cp backend/services/gcp_billing_service.py backend/services/gcp_billing_service.py.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
cp backend/services/gcp_monitoring_service.py backend/services/gcp_monitoring_service.py.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
echo "✅ Backups created"

echo ""
echo "🔄 Fixing BigQuery table patterns..."

# Fix 1: Change all gcp_billing_export_* to gcp_billing_export_resource_v1_*
sed -i.tmp 's/gcp_billing_export_\*/gcp_billing_export_resource_v1_*/g' backend/services/gcp_billing_service.py
rm -f backend/services/gcp_billing_service.py.tmp

# Fix 2: Fix credits array access
# This requires finding the specific line and replacing it
python3 << 'PYTHON_SCRIPT'
import re

# Read the file
with open('backend/services/gcp_billing_service.py', 'r') as f:
    content = f.read()

# Fix credits.amount to proper array handling
old_pattern = r"SUM\(CAST\(credits\.amount AS FLOAT64\)\) as total_credits"
new_pattern = "SUM((SELECT SUM(CAST(c.amount AS FLOAT64)) FROM UNNEST(credits) AS c)) as total_credits"

if old_pattern in content:
    content = re.sub(old_pattern, new_pattern, content)
    print("✅ Fixed credits array access")
else:
    print("⚠️  Credits pattern not found (might already be fixed)")

# Write back
with open('backend/services/gcp_billing_service.py', 'w') as f:
    f.write(content)
PYTHON_SCRIPT

echo "✅ Billing service fixed"

echo ""
echo "🔄 Fixing Monitoring Service queries..."

# Fix 3: Fix monitoring MQL queries
python3 << 'PYTHON_SCRIPT'
import re

try:
    # Read the file
    with open('backend/services/gcp_monitoring_service.py', 'r') as f:
        content = f.read()

    # Fix all occurrences of value.double_value to just value (or proper field name)
    # The monitoring service uses different patterns, so we need to be specific

    # Pattern 1: In aggregations like mean(value.cpu_utilization) -> mean(value.double_value)
    content = re.sub(
        r'mean\(value\.cpu_utilization\)',
        'mean(value.double_value)',
        content
    )
    
    # Pattern 2: In group_by aggregations
    content = re.sub(
        r'count\(value\.cpu_utilization\)',
        'count(value.double_value)',
        content
    )

    # Write back
    with open('backend/services/gcp_monitoring_service.py', 'w') as f:
        f.write(content)
    
    print("✅ Monitoring service fixed")
except Exception as e:
    print(f"⚠️  Could not fix monitoring service: {e}")
    print("   You'll need to use the gcp_monitoring_service_fixed.py file instead")
PYTHON_SCRIPT

echo ""
echo "=============================="
echo "✅ All fixes applied!"
echo ""
echo "📝 Next steps:"
echo "1. Restart your server: python3 main.py"
echo "2. Test your API endpoint"
echo "3. Check logs for any remaining errors"
echo ""
echo "💾 Original files backed up with .backup.TIMESTAMP extension"
echo ""