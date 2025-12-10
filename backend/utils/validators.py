"""
Validation utilities for AuditAI
"""

from typing import Any, Dict, List
import re
from datetime import datetime

class ValidationError(Exception):
    """Custom validation error"""
    pass

class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_gcp_project_id(project_id: str) -> bool:
        """
        Validate GCP project ID format
        Format: lowercase letters, numbers, hyphens (6-30 chars)
        """
        if not project_id or not isinstance(project_id, str):
            raise ValidationError("Project ID must be a non-empty string")
        
        pattern = r'^[a-z0-9-]{6,30}$'
        if not re.match(pattern, project_id):
            raise ValidationError(
                "Invalid GCP project ID format. "
                "Use lowercase letters, numbers, hyphens (6-30 chars)"
            )
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            raise ValidationError("Email must be a non-empty string")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        return True
    
    @staticmethod
    def validate_resource_type(resource_type: str) -> bool:
        """Validate GCP resource type"""
        valid_types = [
            "compute",
            "storage",
            "database",
            "networking",
            "bigquery",
            "container",
            "other"
        ]
        
        if resource_type not in valid_types:
            raise ValidationError(
                f"Invalid resource type. Must be one of: {', '.join(valid_types)}"
            )
        return True
    
    @staticmethod
    def validate_resource_status(status: str) -> bool:
        """Validate resource status"""
        valid_statuses = [
            "RUNNING",
            "STOPPED",
            "IDLE",
            "ERROR",
            "PENDING",
            "UNKNOWN"
        ]
        
        if status not in valid_statuses:
            raise ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return True
    
    @staticmethod
    def validate_severity_level(severity: str) -> bool:
        """Validate recommendation severity"""
        valid_severities = ["critical", "high", "medium", "low", "info"]
        
        if severity not in valid_severities:
            raise ValidationError(
                f"Invalid severity. Must be one of: {', '.join(valid_severities)}"
            )
        return True
    
    @staticmethod
    def validate_datetime(dt_string: str) -> datetime:
        """Validate and parse ISO format datetime"""
        try:
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except ValueError:
            raise ValidationError(
                f"Invalid datetime format. Use ISO 8601: {dt_string}"
            )
    
    @staticmethod
    def validate_dict_keys(data: Dict, required_keys: List[str]) -> bool:
        """Validate required keys in dictionary"""
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            raise ValidationError(
                f"Missing required keys: {', '.join(missing_keys)}"
            )
        return True
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input
        - Strip whitespace
        - Limit length
        - Remove potentially dangerous characters
        """
        if not isinstance(value, str):
            raise ValidationError("Value must be a string")
        
        # Strip whitespace
        value = value.strip()
        
        # Limit length
        if len(value) > max_length:
            value = value[:max_length]
        
        return value

# Usage examples:
# from utils.validators import Validators, ValidationError
# try:
#     Validators.validate_email("test@example.com")
#     Validators.validate_gcp_project_id("my-project-123")
# except ValidationError as e:
#     print(f"Validation failed: {e}")
