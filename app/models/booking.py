from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from .appliance import Appliance
from .problem import Part


@dataclass
class TimeSlot:
    """Represents an available time slot for booking"""
    date: str
    time: str
    datetime: datetime
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "date": self.date,
            "time": self.time,
            "datetime": self.datetime.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TimeSlot":
        """Create from dictionary"""
        dt = data.get("datetime")
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        return cls(
            date=data["date"],
            time=data["time"],
            datetime=dt
        )


@dataclass
class CostBreakdown:
    """Represents cost breakdown for a booking"""
    technician_fee: float
    parts_total: float
    
    @property
    def total(self) -> float:
        """Calculate total cost"""
        return self.technician_fee + self.parts_total
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "technician_fee": self.technician_fee,
            "parts_total": self.parts_total,
            "total": self.total
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CostBreakdown":
        """Create from dictionary"""
        return cls(
            technician_fee=data["technician_fee"],
            parts_total=data.get("parts_total", 0.0)
        )


@dataclass
class Booking:
    """Represents a technician booking"""
    booking_id: str
    timestamp: datetime
    appliance: Appliance
    problem: str
    customer_name: str
    customer_phone: str
    customer_address: str
    time_slot: TimeSlot
    cost: CostBreakdown
    technician_id: Optional[str] = None
    technician_name: Optional[str] = None
    payment_option: str = "pay_on_visit"  # "pay_now" or "pay_on_visit"
    payment_status: str = "pending"  # "pending", "paid", "cancelled"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "booking_id": self.booking_id,
            "timestamp": self.timestamp.isoformat(),
            "appliance": self.appliance.to_dict(),
            "problem": self.problem,
            "customer": {
                "name": self.customer_name,
                "phone": self.customer_phone,
                "address": self.customer_address
            },
            "time_slot": self.time_slot.to_dict(),
            "cost": self.cost.to_dict(),
            "technician_id": self.technician_id,
            "technician_name": self.technician_name,
            "payment_option": self.payment_option,
            "payment_status": self.payment_status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Booking":
        """Create from dictionary"""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        customer = data.get("customer", {})
        return cls(
            booking_id=data["booking_id"],
            timestamp=timestamp,
            appliance=Appliance.from_dict(data["appliance"]),
            problem=data["problem"],
            customer_name=customer.get("name", ""),
            customer_phone=customer.get("phone", ""),
            customer_address=customer.get("address", ""),
            time_slot=TimeSlot.from_dict(data.get("time_slot", {})),
            cost=CostBreakdown.from_dict(data.get("cost", {})),
            technician_id=data.get("technician_id"),
            technician_name=data.get("technician_name"),
            payment_option=data.get("payment_option", "pay_on_visit"),
            payment_status=data.get("payment_status", "pending")
        )

