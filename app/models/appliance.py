from dataclasses import dataclass
from typing import Optional


@dataclass
class Appliance:
    """Represents an appliance with its identification details"""
    brand: str
    model: str
    serial: Optional[str] = None
    age: Optional[int] = None
    appliance_type: Optional[str] = None  # e.g., "Refrigerator", "TV", "Washing Machine"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "brand": self.brand,
            "model": self.model,
            "serial": self.serial or "",
            "age": self.age,
            "appliance_type": self.appliance_type or ""
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Appliance":
        """Create from dictionary"""
        return cls(
            brand=data.get("brand", ""),
            model=data.get("model", ""),
            serial=data.get("serial"),
            age=data.get("age"),
            appliance_type=data.get("appliance_type")
        )
    
    def is_complete(self) -> bool:
        """Check if appliance has minimum required information"""
        return bool(self.brand and self.model)
    
    def __str__(self) -> str:
        age_text = f", around {self.age} years old" if self.age else ""
        return f"Brand: {self.brand}, Model: {self.model}, Serial: {self.serial or 'Unknown'}{age_text}"

