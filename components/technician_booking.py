"""UI components for technician booking"""
import streamlit as st
from typing import List, Optional
from app.models.technician import Technician
from app.models.booking import TimeSlot
from datetime import datetime, timedelta


def display_technician_card(technician: Technician, index: int, key_prefix: str = "tech"):
    """Display a technician card with details"""
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"### {technician.name}")
            st.markdown(f"**Specialization:** {', '.join(technician.specialization)}")
            st.markdown(f"**Experience:** {technician.experience_years} years")
            st.markdown(f"**Location:** {technician.location}")
        
        with col2:
            st.markdown(f"**Rating:** ⭐ {technician.rating}/5.0")
            st.markdown(f"**Base Fee:** ${technician.base_fee:.2f}")
            st.markdown(f"**Response:** {technician.response_time}")
        
        with col3:
            if st.button("Select", key=f"{key_prefix}_select_{index}", use_container_width=True):
                return technician.id
        
        st.markdown("---")
    
    return None


def display_technician_list(technicians: List[Technician]) -> Optional[str]:
    """Display list of technicians and return selected ID"""
    st.markdown("### Available Technicians")
    st.markdown("Select a technician to book:")
    
    selected_id = None
    for idx, tech in enumerate(technicians):
        result = display_technician_card(tech, idx)
        if result:
            selected_id = result
            break
    
    return selected_id


def display_time_slot_selector(technician: Technician) -> Optional[dict]:
    """Display time slot selector for selected technician"""
    st.markdown(f"### Select Time Slot for {technician.name}")
    
    # Get available slots for next 7 days
    today = datetime.now()
    available_slots = []
    
    for day_offset in range(1, 8):
        date = today + timedelta(days=day_offset)
        day_name = date.strftime("%A")
        
        # Find slots for this day
        for ts in technician.time_slots:
            if ts.day == day_name:
                for slot_time in ts.slots:
                    slot_date_str = date.strftime("%B %d, %Y")
                    available_slots.append({
                        "date": slot_date_str,
                        "day": day_name,
                        "time": slot_time,
                        "datetime": date
                    })
    
    if not available_slots:
        st.warning("No available time slots for this technician.")
        return None
    
    # Display as selectbox
    slot_options = [f"{s['date']} - {s['time']}" for s in available_slots]
    selected_index = st.selectbox(
        "Choose a time slot:",
        range(len(slot_options)),
        format_func=lambda x: slot_options[x],
        key="time_slot_select"
    )
    
    if selected_index is not None:
        selected_slot = available_slots[selected_index]
        return {
            "date": selected_slot["date"],
            "time": selected_slot["time"],
            "datetime": selected_slot["datetime"]
        }
    
    return None


def display_payment_options(total_cost: float) -> str:
    """Display payment options and return selected option"""
    st.markdown("### Payment Options")
    st.markdown(f"**Total Cost:** ${total_cost:.2f}")
    
    payment_option = st.radio(
        "Choose payment method:",
        ["Pay Now", "Pay on Visit"],
        key="payment_option"
    )
    
    if payment_option == "Pay Now":
        st.info("💳 You will be redirected to payment after confirmation.")
        return "pay_now"
    else:
        st.info("💰 Payment will be collected when the technician visits.")
        return "pay_on_visit"


def display_booking_summary(
    technician: Technician,
    time_slot: dict,
    customer_info: dict,
    appliance_info: dict,
    issue_summary: str,
    total_cost: float,
    payment_option: str
):
    """Display booking summary before confirmation"""
    st.markdown("### 📋 Booking Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Technician:**")
        st.write(f"- Name: {technician.name}")
        st.write(f"- Rating: ⭐ {technician.rating}/5.0")
        st.write(f"- Fee: ${technician.base_fee:.2f}")
        
        st.markdown("**Time Slot:**")
        st.write(f"- Date: {time_slot['date']}")
        st.write(f"- Time: {time_slot['time']}")
        
        st.markdown("**Appliance:**")
        st.write(f"- Type: {appliance_info.get('appliance_type', 'N/A')}")
        st.write(f"- Brand: {appliance_info.get('brand', 'N/A')}")
        st.write(f"- Model: {appliance_info.get('model', 'N/A')}")
    
    with col2:
        st.markdown("**Customer:**")
        st.write(f"- Name: {customer_info.get('name', 'N/A')}")
        st.write(f"- Phone: {customer_info.get('phone', 'N/A')}")
        st.write(f"- Address: {customer_info.get('address', 'N/A')}")
        
        st.markdown("**Issue:**")
        st.write(issue_summary)
        
        st.markdown("**Payment:**")
        st.write(f"- Option: {'Pay Now' if payment_option == 'pay_now' else 'Pay on Visit'}")
        st.write(f"- Total: ${total_cost:.2f}")
    
    st.markdown("---")
