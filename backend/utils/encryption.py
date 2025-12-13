"""
Encryption utilities for sensitive user data
ONLY for GCP credentials - NOT for passwords
Passwords are handled by AuthService with bcrypt
"""

import json
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet
from config.settings import settings

logger = logging.getLogger(__name__)


class CredentialEncryption:
    """
    Encrypt and decrypt GCP service account credentials
    Uses Fernet (symmetric encryption) for credentials storage
    
    NOTE: Do NOT use this for passwords!
    Passwords use bcrypt in AuthService
    """

    def __init__(self):
        """Initialize encryption with key from settings"""
        try:
            self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            logger.info("✅ Credential encryption initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize encryption: {e}")
            raise

    def encrypt(self, credentials: Dict[str, Any]) -> str:
        """
        Encrypt GCP credentials dictionary
        
        Args:
            credentials: Dictionary containing GCP service account JSON
        
        Returns:
            Encrypted string (safe to store in database)
        
        Example:
            encryptor = CredentialEncryption()
            encrypted = encryptor.encrypt({
                "project_id": "my-project",
                "service_account_json": "{...}",
                "api_key": "..."
            })
        """
        try:
            # Convert dict to JSON string
            json_str = json.dumps(credentials)
            
            # Encrypt
            encrypted_bytes = self.cipher.encrypt(json_str.encode())
            encrypted_str = encrypted_bytes.decode()
            
            logger.info("✅ Credentials encrypted successfully")
            return encrypted_str
        
        except Exception as e:
            logger.error(f"❌ Failed to encrypt credentials: {e}")
            raise

    def decrypt(self, encrypted_credentials: str) -> Dict[str, Any]:
        """
        Decrypt GCP credentials string
        
        Args:
            encrypted_credentials: Encrypted string from database
        
        Returns:
            Dictionary with decrypted GCP credentials
        
        Example:
            encryptor = CredentialEncryption()
            credentials = encryptor.decrypt(encrypted_str)
            project_id = credentials["project_id"]
        """
        try:
            # Decrypt
            decrypted_bytes = self.cipher.decrypt(encrypted_credentials.encode())
            json_str = decrypted_bytes.decode()
            
            # Convert JSON string to dict
            credentials = json.loads(json_str)
            
            logger.info("✅ Credentials decrypted successfully")
            return credentials
        
        except Exception as e:
            logger.error(f"❌ Failed to decrypt credentials: {e}")
            raise


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example: Encrypt and decrypt GCP credentials
    encryptor = CredentialEncryption()
    
    # Original credentials
    original = {
        "project_id": "my-gcp-project",
        "service_account_json": '{"type": "service_account", ...}',
        "api_key": "AIzaSy..."
    }
    
    # Encrypt
    encrypted = encryptor.encrypt(original)
    print(f"Encrypted: {encrypted[:50]}...")
    
    # Decrypt
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    assert original == decrypted
    print("✅ Encryption/Decryption working correctly!")