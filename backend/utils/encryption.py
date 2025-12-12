"""
Encryption utilities for sensitive user data
Encrypts GCP credentials before storing in database
"""

import json
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet
from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CredentialEncryption:
    """
    Encrypt and decrypt sensitive user credentials
    Uses Fernet (symmetric encryption) for GCP credentials
    """

    def __init__(self):
        """Initialize encryption with key from settings"""
        try:
            self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            logger.info("Encryption initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {str(e)}")
            raise

    def encrypt(self, credentials: Dict[str, Any]) -> str:
        """
        Encrypt credentials dictionary
        
        Args:
            credentials: Dictionary containing GCP credentials
        
        Returns:
            Encrypted string (can be stored in database)
        """
        try:
            json_str = json.dumps(credentials)
            encrypted_bytes = self.cipher.encrypt(json_str.encode())
            encrypted_str = encrypted_bytes.decode()
            
            logger.info("Credentials encrypted successfully")
            return encrypted_str
        
        except Exception as e:
            logger.error(f"Failed to encrypt credentials: {str(e)}")
            raise

    def decrypt(self, encrypted_credentials: str) -> Dict[str, Any]:
        """
        Decrypt credentials string
        
        Args:
            encrypted_credentials: Encrypted string from database
        
        Returns:
            Dictionary with decrypted credentials
        """
        try:
            decrypted_bytes = self.cipher.decrypt(encrypted_credentials.encode())
            json_str = decrypted_bytes.decode()
            credentials = json.loads(json_str)
            
            logger.info("Credentials decrypted successfully")
            return credentials
        
        except Exception as e:
            logger.error(f"Failed to decrypt credentials: {str(e)}")
            raise


class PasswordEncryption:
    """Hash and verify passwords using bcrypt"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        import bcrypt
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode(), hashed.encode())