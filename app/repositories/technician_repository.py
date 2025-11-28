"""Repository for technician data"""
import json
from typing import List, Optional
from pathlib import Path
from app.models.technician import Technician


class TechnicianRepository:
    """Repository for accessing technician data"""
    
    def __init__(self, file_path: str = "data/technicians.json"):
        self.file_path = Path(file_path)
        self._cache: Optional[List[Technician]] = None
    
    def load_all(self) -> List[Technician]:
        """Load all technicians from file"""
        if self._cache is not None:
            return self._cache
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cache = [Technician.from_dict(t) for t in data]
                return self._cache
        except FileNotFoundError:
            raise FileNotFoundError(f"Technician data file not found: {self.file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in technician file: {e}")
    
    def get_by_id(self, technician_id: str) -> Optional[Technician]:
        """Get technician by ID"""
        technicians = self.load_all()
        for tech in technicians:
            if tech.id == technician_id:
                return tech
        return None
    
    def get_available_for_appliance(self, appliance_type: str) -> List[Technician]:
        """Get technicians available for a specific appliance type"""
        technicians = self.load_all()
        return [tech for tech in technicians if tech.is_available_for(appliance_type)]
    
    def clear_cache(self):
        """Clear the cache"""
        self._cache = None

