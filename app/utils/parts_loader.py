"""Utility to load parts from image folders based on issue names"""
import re
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image


class PartsLoader:
    """Loads parts from image folders based on issue names"""
    
    # Mapping of issue names to folder names
    ISSUE_TO_FOLDER = {
        "Lights Not Working Inside": "Lights Not Working Images",
        "Water Leakage Inside / Outside": "Water Leakage",
        "Door Not Sealing Properly": "Door Not Sealing Properly"
    }
    
    # Image extensions to look for
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    @staticmethod
    def get_folder_for_issue(issue_name: str) -> Optional[str]:
        """Get folder name for a given issue"""
        # Try exact match first
        if issue_name in PartsLoader.ISSUE_TO_FOLDER:
            return PartsLoader.ISSUE_TO_FOLDER[issue_name]
        
        # Try case-insensitive match
        issue_lower = issue_name.lower()
        for key, folder in PartsLoader.ISSUE_TO_FOLDER.items():
            if key.lower() == issue_lower:
                return folder
        
        # Try partial match
        for key, folder in PartsLoader.ISSUE_TO_FOLDER.items():
            if key.lower() in issue_lower or issue_lower in key.lower():
                return folder
        
        return None
    
    @staticmethod
    def parse_part_info_from_filename(filename: str) -> Optional[Dict]:
        """
        Parse part name and price from filename
        Format: "{Part_Name} - Price $XX.XX.{ext}"
        """
        # Remove extension
        name_without_ext = Path(filename).stem
        
        # Pattern to match: "Part Name - Price $XX.XX" or "Part Name - Price$XX.XX"
        # Handles both with and without space between Price and $
        pattern = r'^(.+?)\s*-\s*Price\s*\$\s*([\d.]+)$'
        match = re.match(pattern, name_without_ext)
        
        # If first pattern doesn't match, try without space between Price and $
        if not match:
            pattern = r'^(.+?)\s*-\s*Price\$\s*([\d.]+)$'
            match = re.match(pattern, name_without_ext)
        
        if match:
            part_name = match.group(1).strip()
            try:
                price = float(match.group(2).strip())
                return {
                    "name": part_name,
                    "price": price,
                    "filename": filename
            }
            except ValueError:
                return None
        
        return None
    
    @staticmethod
    def load_parts_for_issue(issue_name: str, base_dir: Optional[Path] = None) -> List[Dict]:
        """
        Load all parts for a given issue from its folder
        
        Args:
            issue_name: Name of the issue
            base_dir: Base directory path (defaults to current working directory)
        
        Returns:
            List of part dictionaries with name, price, filename, and image_path
        """
        if base_dir is None:
            base_dir = Path.cwd()
        
        folder_name = PartsLoader.get_folder_for_issue(issue_name)
        if not folder_name:
            return []
        
        folder_path = base_dir / folder_name
        if not folder_path.exists():
            return []
        
        parts = []
        
        try:
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix in PartsLoader.IMAGE_EXTENSIONS:
                    part_info = PartsLoader.parse_part_info_from_filename(file_path.name)
                    if part_info:
                        part_info["image_path"] = str(file_path.resolve())
                        parts.append(part_info)
        except Exception as e:
            print(f"Error loading parts from {folder_path}: {e}")
        
        return parts
    
    @staticmethod
    def is_special_issue(issue_name: str) -> bool:
        """Check if this is one of the special issues with part images"""
        return PartsLoader.get_folder_for_issue(issue_name) is not None

