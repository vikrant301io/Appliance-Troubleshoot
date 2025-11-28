import json
from typing import Dict, List, Optional
from pathlib import Path
from app.models.problem import Problem


class KnowledgeBaseRepository:
    """Repository for accessing knowledge base data"""
    
    def __init__(self, file_path: str = "data/knowledge_base.json"):
        self.file_path = Path(file_path)
        self._cache: Optional[Dict] = None
    
    def load(self) -> Dict:
        """Load knowledge base from file"""
        if self._cache is not None:
            return self._cache
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
                return self._cache
        except FileNotFoundError:
            raise FileNotFoundError(f"Knowledge base file not found: {self.file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in knowledge base file: {e}")
    
    def get_problems(self) -> List[Problem]:
        """Get all problems from knowledge base"""
        data = self.load()
        return [Problem.from_dict(p) for p in data.get("problems", [])]
    
    def get_dangerous_keywords(self) -> List[str]:
        """Get list of dangerous keywords"""
        data = self.load()
        return data.get("dangerous_keywords", [])
    
    def get_technician_fee(self) -> float:
        """Get technician visit fee"""
        data = self.load()
        return data.get("technician_fee", 125.0)
    
    def clear_cache(self):
        """Clear the cache (useful for testing or reloading)"""
        self._cache = None

