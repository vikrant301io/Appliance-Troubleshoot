from typing import Dict, Optional, Tuple
from app.models.appliance import Appliance
from app.services.openai_service import OpenAIService


class ApplianceService:
    """Service for appliance identification and management"""
    
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
    
    def identify_from_text(self, text: str) -> Dict:
        """Identify appliance from text input"""
        try:
            info = self.openai_service.extract_appliance_info(text)
            return info
        except Exception as e:
            return {}
    
    def identify_from_image(self, image_bytes: bytes) -> Tuple[str, Dict]:
        """Identify appliance from nameplate image"""
        try:
            text_content, info = self.openai_service.read_nameplate_image(image_bytes)
            return text_content, info
        except Exception as e:
            return "", {}
    
    def update_appliance_info(self, appliance: Appliance, updates: Dict) -> Appliance:
        """Update appliance information with new data"""
        if updates.get("brand"):
            appliance.brand = updates["brand"]
        if updates.get("model"):
            appliance.model = updates["model"]
        if updates.get("serial"):
            appliance.serial = updates["serial"]
        if updates.get("age"):
            appliance.age = updates["age"]
        return appliance
    
    def format_appliance_summary(self, appliance: Appliance) -> str:
        """Format appliance information for display"""
        age_text = f", around {appliance.age} years old" if appliance.age else ""
        return f"""**Brand:** {appliance.brand}
**Model:** {appliance.model}
**Serial:** {appliance.serial or 'Unknown'}{age_text}"""

