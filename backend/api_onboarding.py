"""
Enhanced Onboarding API Endpoints
Helps users connect their GCP accounts smoothly with validation and guidance
"""

from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Body, Form
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
import logging

from models.repositories import UserRepository
from middleware.auth import get_current_user
from services.auth_service import AuthService
from utils.encryption import CredentialEncryption
from utils.validators import Validators
from gcp_client import GCPClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class OnboardingStatusResponse(BaseModel):
    """User onboarding status"""
    is_registered: bool
    has_gcp_credentials: bool
    credentials_valid: bool
    onboarding_complete: bool
    next_step: str
    progress_percentage: int


class GCPSetupGuideResponse(BaseModel):
    """Step-by-step GCP setup guide"""
    steps: List[Dict[str, Any]]
    required_roles: List[str]
    estimated_time_minutes: int


class CredentialsValidationRequest(BaseModel):
    """Request body for credentials validation"""
    project_id: str = Field(..., description="GCP Project ID")
    service_account_json: str = Field(..., description="Service account JSON as string")


class CredentialsValidationResponse(BaseModel):
    """Credentials validation result"""
    is_valid: bool
    project_id: Optional[str]
    issues: List[str]
    suggestions: List[str]


# ============================================================================
# ONBOARDING STATUS ENDPOINTS
# ============================================================================

@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(user_id: str = Depends(get_current_user)):
    """
    Get user's onboarding status and next steps
    
    Returns:
        - Progress percentage (0-100)
        - Next action to take
        - What's completed, what's pending
    
    Example Response:
        {
            "is_registered": true,
            "has_gcp_credentials": true,
            "credentials_valid": false,
            "onboarding_complete": false,
            "next_step": "verify_credentials",
            "progress_percentage": 50
        }
    """
    try:
        logger.info(f"Getting onboarding status for user: {user_id}")
        
        # Get user from database
        user = UserRepository.find_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check onboarding progress
        is_registered = True  # They're authenticated
        has_gcp_credentials = user.gcp_credentials is not None
        credentials_valid = False
        
        # Verify credentials if they exist
        if has_gcp_credentials:
            try:
                encryptor = CredentialEncryption()
                creds = encryptor.decrypt(user.gcp_credentials)
                gcp_client = GCPClient(creds['project_id'])
                credentials_valid = gcp_client.verify_credentials()
            except Exception as e:
                logger.error(f"Credential validation error: {e}")
                credentials_valid = False
        
        onboarding_complete = is_registered and has_gcp_credentials and credentials_valid
        
        # Determine next step
        if not has_gcp_credentials:
            next_step = "add_gcp_credentials"
            progress = 33
        elif not credentials_valid:
            next_step = "verify_credentials"
            progress = 66
        else:
            next_step = "start_analysis"
            progress = 100
        
        return OnboardingStatusResponse(
            is_registered=is_registered,
            has_gcp_credentials=has_gcp_credentials,
            credentials_valid=credentials_valid,
            onboarding_complete=onboarding_complete,
            next_step=next_step,
            progress_percentage=progress
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get onboarding status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get onboarding status"
        )


# ============================================================================
# GCP SETUP GUIDE
# ============================================================================

@router.get("/gcp-setup-guide", response_model=GCPSetupGuideResponse)
async def get_gcp_setup_guide():
    """
    Get detailed step-by-step guide for GCP setup
    
    Returns complete instructions for:
    1. Finding project ID
    2. Creating service account
    3. Granting permissions
    4. Downloading JSON key
    """
    try:
        steps = [
            {
                "step_number": 1,
                "title": "Go to GCP Console",
                "description": "Open Google Cloud Console in a new tab",
                "action": "Visit https://console.cloud.google.com/",
                "link": "https://console.cloud.google.com/",
                "estimated_minutes": 1
            },
            {
                "step_number": 2,
                "title": "Select Your Project",
                "description": "Choose the GCP project you want to audit",
                "action": "Click the project dropdown at the top, select your project",
                "tip": "If you don't have a project, create one first",
                "estimated_minutes": 1
            },
            {
                "step_number": 3,
                "title": "Copy Project ID",
                "description": "Find and copy your project ID",
                "action": "Project ID is shown in the project dropdown (e.g., 'my-project-123')",
                "tip": "Not the project name - the Project ID is unique",
                "estimated_minutes": 1
            },
            {
                "step_number": 4,
                "title": "Enable Required APIs",
                "description": "Enable the APIs we need to audit your infrastructure",
                "action": "Go to APIs & Services > Library, search and enable:\n- Compute Engine API\n- Cloud Billing API\n- Cloud Monitoring API\n- Recommender API\n- BigQuery API",
                "link": "https://console.cloud.google.com/apis/library",
                "estimated_minutes": 3
            },
            {
                "step_number": 5,
                "title": "Create Service Account",
                "description": "Create a dedicated service account for AuditAI",
                "action": "1. Go to IAM & Admin > Service Accounts\n2. Click 'Create Service Account'\n3. Name: 'auditai-service'\n4. Description: 'Service account for AuditAI auditing'\n5. Click 'Create and Continue'",
                "link": "https://console.cloud.google.com/iam-admin/serviceaccounts",
                "estimated_minutes": 2
            },
            {
                "step_number": 6,
                "title": "Grant Required Roles",
                "description": "Give the service account permission to read your infrastructure",
                "action": "Grant these roles:\n- Viewer\n- Cloud Asset Viewer\n- Billing Account Viewer\n- Monitoring Viewer\n- Recommender Viewer",
                "tip": "These are read-only roles - AuditAI cannot modify your resources",
                "estimated_minutes": 2
            },
            {
                "step_number": 7,
                "title": "Create JSON Key",
                "description": "Generate a key file for authentication",
                "action": "1. Click on your service account\n2. Go to 'Keys' tab\n3. Click 'Add Key' > 'Create new key'\n4. Choose 'JSON'\n5. Click 'Create'",
                "tip": "The JSON file will download automatically - keep it safe!",
                "estimated_minutes": 2
            },
            {
                "step_number": 8,
                "title": "Upload to AuditAI",
                "description": "Connect your GCP account to AuditAI",
                "action": "Return to AuditAI and upload:\n1. Your Project ID\n2. The downloaded JSON key file",
                "estimated_minutes": 1
            }
        ]
        
        required_roles = [
            "roles/viewer",
            "roles/cloudasset.viewer",
            "roles/billing.viewer",
            "roles/monitoring.viewer",
            "roles/recommender.viewer"
        ]
        
        total_time = sum(step.get('estimated_minutes', 0) for step in steps)
        
        return GCPSetupGuideResponse(
            steps=steps,
            required_roles=required_roles,
            estimated_time_minutes=total_time
        )
    
    except Exception as e:
        logger.error(f"Failed to get setup guide: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get setup guide"
        )


# ============================================================================
# CREDENTIALS VALIDATION (BEFORE SAVING)
# ============================================================================
@router.post("/test-upload")
async def test_upload(
    project_id: str = Form(None),
    file: UploadFile = File(None)
):
    """TEST ENDPOINT - No auth, just test"""
    return {
        "received_project_id": project_id,
        "received_file": file.filename if file else None,
        "file_is_none": file is None,
        "project_id_is_none": project_id is None
    }

@router.post("/validate-credentials")
async def validate_credentials_before_save(
    # Option 1: Form-data parameters
    project_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    # Option 2: JSON body (for backward compatibility)
    request: Optional[CredentialsValidationRequest] = None,
    user_id: str = Depends(get_current_user)
):
    """
    Validate GCP credentials BEFORE saving them
    
    Accepts TWO formats:
    
    **Format 1: Form-data (RECOMMENDED)**
    - project_id: Text field
    - file: Upload your service-account.json file
    
    **Format 2: JSON body (Legacy)**
    - project_id: string
    - service_account_json: escaped JSON string
    
    Returns:
    - is_valid: boolean
    - project_id: string (if valid)
    - issues: list of problems found
    - suggestions: list of recommendations
    """
    try:
        logger.info(f"Validating credentials for user: {user_id}")
        
        issues = []
        suggestions = []
        sa_dict = None
        final_project_id = None
        service_account_json = None
        
        # ============================================================
        # DETERMINE INPUT FORMAT
        # ============================================================
        
        # Check if form-data was provided
        if file is not None and project_id is not None:
            logger.info("📄 Processing form-data input")
            
            # Validate file type
            if not file.filename.endswith('.json'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File must be a .json file"
                )
            
            # Read file content
            content = await file.read()
            
            try:
                service_account_json = content.decode('utf-8')
                sa_dict = json.loads(service_account_json)
                final_project_id = project_id
                logger.info(f"✅ Successfully parsed uploaded JSON file")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File encoding error - ensure it's a UTF-8 text file"
                )
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid JSON file format"
                )
        
        # Check if JSON body was provided
        elif request is not None:
            logger.info("📝 Processing JSON body input")
            final_project_id = request.project_id
            service_account_json = request.service_account_json
            
            try:
                sa_dict = json.loads(service_account_json)
            except json.JSONDecodeError:
                issues.append("Invalid JSON format in service_account_json field")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either provide (project_id + file) as form-data OR (project_id + service_account_json) as JSON"
            )
        
        # ============================================================
        # VALIDATE PROJECT ID FORMAT
        # ============================================================
        
        try:
            Validators.validate_gcp_project_id(final_project_id)
        except Exception as e:
            issues.append(f"Invalid project ID format: {str(e)}")
        
        # ============================================================
        # VALIDATE SERVICE ACCOUNT JSON STRUCTURE
        # ============================================================
        
        if sa_dict:
            # Check required fields
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [f for f in required_fields if f not in sa_dict]
            
            if missing_fields:
                issues.append(f"Service account JSON missing fields: {', '.join(missing_fields)}")
            
            # Validate type
            if sa_dict.get('type') != 'service_account':
                issues.append("JSON must be a service account (type='service_account')")
            
            # Check if project IDs match
            json_project_id = sa_dict.get('project_id')
            if json_project_id != final_project_id:
                issues.append(
                    f"Project ID mismatch: You entered '{final_project_id}' but JSON contains '{json_project_id}'"
                )
                suggestions.append(f"Use project ID: {json_project_id}")
        
        # ============================================================
        # TEST GCP API ACCESS
        # ============================================================
        
        if not issues and sa_dict:
            try:
                logger.info(f"🔍 Testing GCP API access for project: {final_project_id}")
                
                # Initialize GCP client with the service account dict
                gcp_client = GCPClient(
                    project_id=final_project_id,
                    service_account_info=sa_dict
                )
                
                # Verify credentials
                if not gcp_client.verify_credentials():
                    issues.append("Failed to authenticate with GCP - credentials may be invalid")
                    suggestions.append("Ensure the service account has 'Viewer' role")
                    suggestions.append("Check that required APIs are enabled in GCP Console")
                else:
                    logger.info("✅ GCP credentials validated successfully")
                    suggestions.append("Credentials are valid!")
                    suggestions.append("You can proceed to save them using /upload-service-account")
            
            except Exception as e:
                logger.error(f"❌ GCP authentication failed: {e}")
                issues.append(f"GCP authentication failed: {str(e)}")
                suggestions.append("Verify the service account has necessary permissions")
                suggestions.append("Check that all required APIs are enabled:")
                suggestions.append("  - Compute Engine API")
                suggestions.append("  - Cloud Billing API")
                suggestions.append("  - Cloud Monitoring API")
        
        # ============================================================
        # RETURN VALIDATION RESULT
        # ============================================================
        
        is_valid = len(issues) == 0
        
        return {
            "is_valid": is_valid,
            "project_id": final_project_id if is_valid else None,
            "service_account_email": sa_dict.get('client_email') if sa_dict else None,
            "issues": issues,
            "suggestions": suggestions,
            "validation_method": "form-data" if file else "json-body"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate credentials: {str(e)}"
        )


# ============================================================================
# FILE UPLOAD ENDPOINT (Alternative to JSON string)
# ============================================================================

@router.post("/upload-service-account")
async def upload_service_account_file(
    user_id: str = Depends(get_current_user),
    project_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload service account JSON file directly"""
    try:
        logger.info(f"Processing file upload for user: {user_id}")
        logger.info(f"Received project_id: {project_id}")
        logger.info(f"Received file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a .json file"
            )
        
        # Read file content
        content = await file.read()
        
        try:
            service_account_json = content.decode('utf-8')
            sa_dict = json.loads(service_account_json)
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File encoding error - ensure it's a UTF-8 text file"
            )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON file format"
            )
        
        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [f for f in required_fields if f not in sa_dict]
        
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service account JSON missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate it's a service account
        if sa_dict.get('type') != 'service_account':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON must be a service account (type='service_account')"
            )
        
        # Validate project IDs match
        json_project_id = sa_dict.get('project_id')
        if json_project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project ID mismatch: You entered '{project_id}' but JSON contains '{json_project_id}'. Please use '{json_project_id}'"
            )
        
        # Validate GCP credentials
        try:
            logger.info(f"Validating GCP credentials for project: {project_id}")
            
            gcp_client = GCPClient(
                project_id=project_id,
                service_account_info=sa_dict
            )
            
            if not gcp_client.verify_credentials():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="GCP credentials are invalid or lack required permissions"
                )
            
            logger.info(f"✅ GCP credentials validated successfully")
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ GCP validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to validate GCP credentials: {str(e)}"
            )
        
        # Encrypt and save credentials
        encryptor = CredentialEncryption()
        encrypted_creds = encryptor.encrypt({
            "project_id": project_id,
            "service_account_json": service_account_json
        })
        
        # Save to database
        UserRepository.add_gcp_credentials(
            user_id=user_id,
            project_id=project_id,
            encrypted_credentials=encrypted_creds
        )
        
        logger.info(f"✅ GCP credentials saved for user: {user_id}")
        
        return {
            "status": "success",
            "message": "GCP credentials saved successfully",
            "project_id": project_id,
            "service_account_email": sa_dict.get('client_email'),
            "validation": "passed"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ File upload failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file upload: {str(e)}"
        )



# ============================================================================
# HELPER ENDPOINT: Check GCP Permissions
# ============================================================================

@router.get("/check-permissions")
async def check_gcp_permissions(user_id: str = Depends(get_current_user)):
    """
    Check which GCP permissions the service account has
    
    Tests APIs by actually trying to access them through your GCPClient.
    Returns detailed breakdown of accessible vs inaccessible APIs.
    """
    try:
        logger.info(f"Checking GCP permissions for user: {user_id}")
        
        # Get user from database
        user = UserRepository.find_by_id(user_id)
        
        if not user or not user.gcp_credentials:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No GCP credentials configured. Please upload credentials first."
            )
        
        # Decrypt credentials
        encryptor = CredentialEncryption()
        creds = encryptor.decrypt(user.gcp_credentials)
        
        # Parse service account JSON
        service_account_json = creds.get('service_account_json')
        if isinstance(service_account_json, str):
            sa_dict = json.loads(service_account_json)
        else:
            sa_dict = service_account_json
        
        project_id = creds.get('project_id') or user.gcp_project_id
        
        # Initialize GCP client
        gcp_client = GCPClient(
            project_id=project_id,
            service_account_info=sa_dict
        )
        
        # Verify basic credentials
        credentials_valid = gcp_client.verify_credentials()
        
        if not credentials_valid:
            return {
                "status": "error",
                "project_id": project_id,
                "service_account_email": sa_dict.get('client_email'),
                "credentials_valid": False,
                "message": "❌ Credentials are invalid. Please re-upload your service account JSON.",
                "permissions": {},
                "health_percentage": 0,
                "enabled_apis": 0,
                "total_apis": 0
            }
        
        # Test available APIs using methods that exist in your GCPClient
        permissions_status = {}
        api_details = {}
        
        # Map of API names to their test methods
        api_tests = {
            "compute": {
                "method": "fetch_compute_instances",
                "description": "Compute Engine API - VM instances",
                "required_for": ["Infrastructure analysis", "Cost optimization"],
                "enable_url": f"https://console.cloud.google.com/apis/library/compute.googleapis.com?project={project_id}"
            },
            "storage": {
                "method": "fetch_storage_buckets",
                "description": "Cloud Storage API - Storage buckets",
                "required_for": ["Storage analysis", "Cost optimization"],
                "enable_url": f"https://console.cloud.google.com/apis/library/storage.googleapis.com?project={project_id}"
            },
            "billing": {
                "method": "fetch_billing_data",
                "description": "Cloud Billing API - Cost data",
                "required_for": ["Cost analysis", "Budget tracking"],
                "enable_url": f"https://console.cloud.google.com/apis/library/cloudbilling.googleapis.com?project={project_id}",
                "optional": True  # Mark as optional if method doesn't exist
            },
            "monitoring": {
                "method": "fetch_resource_metrics",
                "description": "Cloud Monitoring API - Metrics and performance",
                "required_for": ["Performance analysis", "Resource optimization"],
                "enable_url": f"https://console.cloud.google.com/apis/library/monitoring.googleapis.com?project={project_id}",
                "optional": True
            },
            "recommender": {
                "method": "fetch_recommendations",
                "description": "Recommender API - AI suggestions",
                "required_for": ["AI-powered recommendations"],
                "enable_url": f"https://console.cloud.google.com/apis/library/recommender.googleapis.com?project={project_id}",
                "optional": True
            }
        }
        
        # Test each API
        for api_name, api_config in api_tests.items():
            method_name = api_config["method"]
            
            # Check if method exists
            if not hasattr(gcp_client, method_name):
                if api_config.get("optional"):
                    # Skip optional APIs that aren't implemented yet
                    logger.info(f"Skipping optional API: {api_name} (method not implemented)")
                    continue
                else:
                    permissions_status[api_name] = False
                    api_details[api_name] = {
                        "accessible": False,
                        "error": "Method not implemented in GCPClient",
                        "description": api_config["description"]
                    }
                    continue
            
            # Try to call the method
            try:
                method = getattr(gcp_client, method_name)
                
                # Call with appropriate parameters
                if method_name == "fetch_billing_data":
                    result = method(days=7)
                else:
                    result = method()
                
                permissions_status[api_name] = True
                api_details[api_name] = {
                    "accessible": True,
                    "description": api_config["description"],
                    "required_for": api_config["required_for"]
                }
                logger.info(f"✅ {api_name} API: Accessible")
                
            except Exception as e:
                permissions_status[api_name] = False
                error_message = str(e)
                
                # Provide helpful error messages
                if "403" in error_message or "permission" in error_message.lower():
                    help_text = "Service account lacks required permissions"
                elif "404" in error_message or "not found" in error_message.lower():
                    help_text = "API not enabled in GCP Console"
                elif "401" in error_message or "unauthorized" in error_message.lower():
                    help_text = "Authentication failed"
                else:
                    help_text = "API not accessible"
                
                api_details[api_name] = {
                    "accessible": False,
                    "error": help_text,
                    "description": api_config["description"],
                    "required_for": api_config["required_for"],
                    "enable_url": api_config["enable_url"]
                }
                logger.warning(f"❌ {api_name} API: {help_text} - {error_message}")
        
        # Calculate health percentage
        enabled_count = sum(1 for v in permissions_status.values() if v)
        total_count = len(permissions_status)
        health_percentage = int((enabled_count / total_count) * 100) if total_count > 0 else 0
        
        # Generate recommendations
        recommendations = []
        
        for api_name, details in api_details.items():
            if not details.get("accessible"):
                recommendations.append({
                    "api": api_name,
                    "description": details["description"],
                    "action": "Enable this API in GCP Console",
                    "enable_url": details.get("enable_url"),
                    "required_for": details.get("required_for", [])
                })
        
        # Determine status message
        if health_percentage == 100:
            status_message = "✅ Perfect! All APIs are accessible."
        elif health_percentage >= 60:
            status_message = f"⚠️ Partial access: {enabled_count}/{total_count} APIs accessible."
        elif health_percentage >= 40:
            status_message = f"⚠️ Limited access: {enabled_count}/{total_count} APIs accessible. Enable more APIs for full functionality."
        else:
            status_message = f"❌ Poor access: Only {enabled_count}/{total_count} APIs accessible. Please enable required APIs."
        
        logger.info(f"Permission check completed: {health_percentage}% health ({enabled_count}/{total_count} APIs)")
        
        return {
            "status": "success",
            "message": status_message,
            "project_id": project_id,
            "service_account_email": sa_dict.get('client_email'),
            "credentials_valid": credentials_valid,
            "permissions": permissions_status,
            "api_details": api_details,
            "health_percentage": health_percentage,
            "enabled_apis": enabled_count,
            "total_apis": total_count,
            "recommendations": recommendations,
            "next_steps": [
                "Enable missing APIs in GCP Console" if recommendations else "All required APIs are enabled",
                "Grant additional roles to service account if needed",
                "Test again after making changes"
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission check failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check permissions: {str(e)}"
        )

@router.get("/check-permissions-debug")
async def check_gcp_permissions_debug(
    api: Optional[str] = None,  # Query param: ?api=compute
    user_id: str = Depends(get_current_user)
):
    """
    DEBUG ENDPOINT - Test individual APIs
    
    Usage:
    - /check-permissions-debug?api=compute
    - /check-permissions-debug?api=storage
    - /check-permissions-debug?api=billing
    - /check-permissions-debug (tests verify_credentials only)
    """
    try:
        logger.info(f"🐛 DEBUG: Starting for user {user_id}, api={api}")
        
        # Step 1: Get user
        logger.info("🐛 Step 1: Fetching user...")
        user = UserRepository.find_by_id(user_id)
        if not user or not user.gcp_credentials:
            return {"error": "No credentials"}
        logger.info("✅ Step 1: User found")
        
        # Step 2: Decrypt
        logger.info("🐛 Step 2: Decrypting...")
        encryptor = CredentialEncryption()
        creds = encryptor.decrypt(user.gcp_credentials)
        logger.info("✅ Step 2: Decrypted")
        
        # Step 3: Parse JSON
        logger.info("🐛 Step 3: Parsing JSON...")
        service_account_json = creds.get('service_account_json')
        if isinstance(service_account_json, str):
            sa_dict = json.loads(service_account_json)
        else:
            sa_dict = service_account_json
        project_id = creds.get('project_id') or user.gcp_project_id
        logger.info(f"✅ Step 3: Parsed, project={project_id}")
        
        # Step 4: Initialize client
        logger.info("🐛 Step 4: Initializing GCP client...")
        from gcp_client import GCPClient
        gcp_client = GCPClient(
            project_id=project_id,
            service_account_info=sa_dict
        )
        logger.info("✅ Step 4: Client initialized")
        
        # If no specific API requested, just verify credentials
        if not api:
            logger.info("🐛 Step 5: Verifying credentials (no specific API)...")
            is_valid = gcp_client.verify_credentials()
            logger.info(f"✅ Step 5: Verification result = {is_valid}")
            return {
                "status": "success",
                "step": "verify_credentials",
                "result": is_valid,
                "project_id": project_id
            }
        
        # Test specific API
        logger.info(f"🐛 Step 5: Testing {api} API...")
        
        result = None
        if api == "compute":
            result = gcp_client.fetch_compute_instances()
        elif api == "storage":
            result = gcp_client.fetch_storage_buckets()
        elif api == "billing":
            result = gcp_client.fetch_billing_data(days=7)
        elif api == "monitoring":
            result = gcp_client.fetch_resource_metrics(hours=1)
        elif api == "recommender":
            result = gcp_client.fetch_recommendations()
        else:
            return {"error": f"Unknown API: {api}"}
        
        logger.info(f"✅ Step 5: {api} API returned data")
        
        return {
            "status": "success",
            "api": api,
            "result_type": type(result).__name__,
            "result_count": len(result) if isinstance(result, (list, dict)) else None,
            "sample": str(result)[:200] if result else None
        }
    
    except Exception as e:
        logger.error(f"🐛 DEBUG ERROR: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


# Export router
__all__ = ["router"]