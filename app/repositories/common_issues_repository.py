"""Repository for common issues data"""
import json
from typing import List, Optional
from pathlib import Path


class CommonIssuesRepository:
    """Repository for accessing common issues data"""
    
    def __init__(self, file_path: str = "data/common_issues.json"):
        self.file_path = Path(file_path)
        self._cache: Optional[dict] = None
    
    def load(self) -> dict:
        """Load common issues from file"""
        if self._cache is not None:
            return self._cache
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
                return self._cache
        except FileNotFoundError:
            raise FileNotFoundError(f"Common issues file not found: {self.file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in common issues file: {e}")
    
    def get_issues_for_type(self, appliance_type: str) -> List[str]:
        """Get common issues for an appliance type"""
        data = self.load()
        return data.get(appliance_type, [])
    
    def clear_cache(self):
        """Clear the cache"""
        self._cache = None

