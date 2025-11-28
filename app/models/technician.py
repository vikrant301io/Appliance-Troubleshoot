"""Technician model for booking system"""
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TechnicianTimeSlot:
    """Time slot for technician availability"""
    day: str
    slots: List[str]
    
    def to_dict(self) -> dict:
        return {"day": self.day, "slots": self.slots}
    
    @classmethod
    def from_dict(cls, data: dict) -> "TechnicianTimeSlot":
        return cls(day=data["day"], slots=data["slots"])


@dataclass
class Technician:
    """Technician information"""
    id: str
    name: str
    specialization: List[str]
    rating: float
    experience_years: int
    base_fee: float
    availability: List[str]
    time_slots: List[TechnicianTimeSlot]
    location: str
    response_time: str
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "rating": self.rating,
            "experience_years": self.experience_years,
            "base_fee": self.base_fee,
            "availability": self.availability,
            "time_slots": [ts.to_dict() for ts in self.time_slots],
            "location": self.location,
            "response_time": self.response_time
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Technician":
        return cls(
            id=data["id"],
            name=data["name"],
            specialization=data["specialization"],
            rating=data["rating"],
            experience_years=data["experience_years"],
            base_fee=data["base_fee"],
            availability=data["availability"],
            time_slots=[TechnicianTimeSlot.from_dict(ts) for ts in data["time_slots"]],
            location=data["location"],
            response_time=data["response_time"]
        )
    
    def is_available_for(self, appliance_type: str) -> bool:
        """Check if technician is available for appliance type"""
        return "All Appliances" in self.specialization or appliance_type in self.specialization

