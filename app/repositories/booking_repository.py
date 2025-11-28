import json
import uuid
from typing import List
from pathlib import Path
from datetime import datetime
from app.models.booking import Booking


class BookingRepository:
    """Repository for managing booking data"""
    
    def __init__(self, file_path: str = "data/bookings.json"):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure bookings file exists, create if it doesn't"""
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def save(self, booking: Booking) -> None:
        """Save a booking to file"""
        bookings = self.load_all()
        bookings.append(booking)
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in bookings], f, indent=2)
    
    def load_all(self) -> List[Booking]:
        """Load all bookings from file"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Booking.from_dict(b) for b in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def get_by_id(self, booking_id: str) -> Booking | None:
        """Get a booking by ID"""
        bookings = self.load_all()
        for booking in bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    @staticmethod
    def generate_booking_id() -> str:
        """Generate a unique booking ID"""
        return str(uuid.uuid4())[:8].upper()

