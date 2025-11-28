from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Part:
    """Represents a replacement part"""
    name: str
    part_number: str
    price: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "part_number": self.part_number,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Part":
        """Create from dictionary"""
        return cls(
            name=data["name"],
            part_number=data["part_number"],
            price=data["price"]
        )


@dataclass
class Problem:
    """Represents a problem with troubleshooting information"""
    id: str
    title: str
    keywords: List[str]
    category: str  # "SIMPLE" or "COMPLEX"
    troubleshooting_steps: List[str]
    parts: List[Part]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "keywords": self.keywords,
            "category": self.category,
            "troubleshooting_steps": self.troubleshooting_steps,
            "parts": [part.to_dict() for part in self.parts]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Problem":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            title=data["title"],
            keywords=data.get("keywords", []),
            category=data.get("category", "COMPLEX"),
            troubleshooting_steps=data.get("troubleshooting_steps", []),
            parts=[Part.from_dict(p) for p in data.get("parts", [])]
        )
    
    def is_simple(self) -> bool:
        """Check if problem is simple (self-fixable)"""
        return self.category == "SIMPLE"
    
    def has_parts(self) -> bool:
        """Check if problem requires parts"""
        return len(self.parts) > 0

