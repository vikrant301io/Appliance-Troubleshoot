import hashlib
from typing import Tuple, Optional, Dict


class ImageUtils:
    """Utility functions for image handling"""
    
    @staticmethod
    def get_image_hash(image_bytes: bytes) -> str:
        """Generate hash for image bytes"""
        return hashlib.md5(image_bytes).hexdigest()
    
    @staticmethod
    def validate_image_format(filename: str, allowed_types: list = None) -> bool:
        """Validate image file format"""
        if allowed_types is None:
            allowed_types = ["jpg", "jpeg", "png"]
        
        extension = filename.split(".")[-1].lower()
        return extension in allowed_types

