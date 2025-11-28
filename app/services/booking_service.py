from typing import List
from datetime import datetime, timedelta
from app.models.booking import TimeSlot, CostBreakdown
from app.models.appliance import Appliance
from app.models.problem import Part
from app.repositories.knowledge_base_repository import KnowledgeBaseRepository


class BookingService:
    """Service for managing booking flow and calculations"""
    
    def __init__(self, knowledge_base_repo: KnowledgeBaseRepository):
        self.knowledge_base_repo = knowledge_base_repo
    
    def generate_time_slots(self, count: int = 4) -> List[TimeSlot]:
        """Generate available time slots"""
        slots = []
        today = datetime.now()
        
        for day_offset in [1, 2]:
            date = today + timedelta(days=day_offset)
            date_str = date.strftime("%B %d, %Y")
            
            slots.append(TimeSlot(
                date=date_str,
                time="10:00 AM - 12:00 PM",
                datetime=date.replace(hour=10, minute=0)
            ))
            slots.append(TimeSlot(
                date=date_str,
                time="2:00 PM - 4:00 PM",
                datetime=date.replace(hour=14, minute=0)
            ))
        
        return slots[:count]
    
    def calculate_cost(self, parts: List[Part]) -> CostBreakdown:
        """Calculate total cost for booking"""
        tech_fee = self.knowledge_base_repo.get_technician_fee()
        parts_total = sum(part.price for part in parts)
        
        return CostBreakdown(
            technician_fee=tech_fee,
            parts_total=parts_total
        )
    
    def format_booking_summary(
        self,
        appliance: Appliance,
        problem: str,
        time_slot: TimeSlot,
        cost: CostBreakdown,
        parts: List[Part]
    ) -> str:
        """Format booking summary for display"""
        parts_text = ""
        if parts:
            parts_text = "\n**Parts:**\n"
            for part in parts:
                parts_text += f"- {part.name} (Part #{part.part_number}): ${part.price:.2f}\n"
        else:
            parts_text = "\n**Parts:** None specified\n"
        
        return f"""**Booking Summary:**

**Appliance:**
- Brand: {appliance.brand}
- Model: {appliance.model}
- Serial: {appliance.serial or 'Unknown'}

**Problem:** {problem}

**Time Slot:** {time_slot.date} - {time_slot.time}

**Cost Breakdown:**
- Technician Fee: ${cost.technician_fee:.2f}
{parts_text}
**Total: ${cost.total:.2f}**"""
    
    def format_confirmation(
        self,
        booking_id: str,
        appliance: Appliance,
        problem: str,
        time_slot: TimeSlot,
        cost: CostBreakdown,
        parts: List[Part]
    ) -> str:
        """Format booking confirmation message"""
        parts_text = ""
        if parts:
            parts_text = "\n**Parts:**\n"
            for part in parts:
                parts_text += f"- {part.name} (Part #{part.part_number}): ${part.price:.2f}\n"
        else:
            parts_text = "\n**Parts:** None specified\n"
        
        return f"""✅ **Booking Confirmed!**

**Booking ID:** {booking_id}

**Appliance:**
- Brand: {appliance.brand}
- Model: {appliance.model}
- Serial: {appliance.serial or 'Unknown'}

**Problem:** {problem}

**Time Slot:** {time_slot.date} - {time_slot.time}

**Cost Breakdown:**
- Technician Fee: ${cost.technician_fee:.2f}
{parts_text}
**Total: ${cost.total:.2f}**

Your technician will arrive at the scheduled time. Thank you for using our service!"""

