import streamlit as st
from typing import Dict, Any, Optional
from app.models.appliance import Appliance
from app.models.problem import Problem, Part


class StateManager:
    """Manages Streamlit session state"""
    
    FLOW_CATEGORY_SELECTION = "category_selection"
    FLOW_IDENTIFICATION = "identification"
    FLOW_ISSUE_LISTING = "issue_listing"
    FLOW_TROUBLESHOOTING = "troubleshooting"
    FLOW_BOOKING = "booking"
    FLOW_PART_ORDERING = "part_ordering"
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "appliance_info" not in st.session_state:
            st.session_state.appliance_info = {}
        if "current_flow" not in st.session_state:
            st.session_state.current_flow = StateManager.FLOW_CATEGORY_SELECTION
        if "problem_description" not in st.session_state:
            st.session_state.problem_description = ""
        if "suggested_parts" not in st.session_state:
            st.session_state.suggested_parts = []
        if "booking_info" not in st.session_state:
            st.session_state.booking_info = {}
        if "vision_cache" not in st.session_state:
            st.session_state.vision_cache = {}
        if "troubleshooting_steps" not in st.session_state:
            st.session_state.troubleshooting_steps = []
        if "processed_images" not in st.session_state:
            st.session_state.processed_images = set()
        if "troubleshooting_stage" not in st.session_state:
            st.session_state.troubleshooting_stage = "symptom_capture"  # symptom_capture, level1, level2, part_suggestion, completed
        if "symptom_data" not in st.session_state:
            st.session_state.symptom_data = {}
        if "current_step_index" not in st.session_state:
            st.session_state.current_step_index = 0
        if "level1_completed" not in st.session_state:
            st.session_state.level1_completed = False
        if "level2_consent" not in st.session_state:
            st.session_state.level2_consent = None
        if "level2_completed" not in st.session_state:
            st.session_state.level2_completed = False
        if "step_responses" not in st.session_state:
            st.session_state.step_responses = {}  # Track YES/NO/Not sure for each step
    
    @staticmethod
    def reset():
        """Reset all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        StateManager.initialize()
    
    @staticmethod
    def get_appliance() -> Optional[Appliance]:
        """Get current appliance from session state"""
        info = st.session_state.get("appliance_info", {})
        if not info:
            return None
        return Appliance.from_dict(info)
    
    @staticmethod
    def set_appliance(appliance: Appliance):
        """Set appliance in session state"""
        st.session_state.appliance_info = appliance.to_dict()
    
    @staticmethod
    def get_current_flow() -> str:
        """Get current flow state"""
        return st.session_state.get("current_flow", StateManager.FLOW_CATEGORY_SELECTION)
    
    @staticmethod
    def set_current_flow(flow: str):
        """Set current flow state"""
        st.session_state.current_flow = flow
    
    @staticmethod
    def get_problem_description() -> str:
        """Get problem description"""
        return st.session_state.get("problem_description", "")
    
    @staticmethod
    def set_problem_description(description: str):
        """Set problem description"""
        st.session_state.problem_description = description
    
    @staticmethod
    def get_suggested_parts() -> list:
        """Get suggested parts"""
        return st.session_state.get("suggested_parts", [])
    
    @staticmethod
    def set_suggested_parts(parts: list):
        """Set suggested parts"""
        st.session_state.suggested_parts = parts
    
    @staticmethod
    def get_troubleshooting_steps() -> list:
        """Get troubleshooting steps"""
        return st.session_state.get("troubleshooting_steps", [])
    
    @staticmethod
    def set_troubleshooting_steps(steps: list):
        """Set troubleshooting steps"""
        st.session_state.troubleshooting_steps = steps
    
    @staticmethod
    def get_booking_info() -> Dict:
        """Get booking information"""
        return st.session_state.get("booking_info", {})
    
    @staticmethod
    def set_booking_info(info: Dict):
        """Set booking information"""
        st.session_state.booking_info = info
    
    @staticmethod
    def add_message(role: str, content: str, image: Optional[bytes] = None):
        """Add message to chat history"""
        message = {"role": role, "content": content}
        if image:
            message["image"] = image
        st.session_state.messages.append(message)
    
    @staticmethod
    def get_messages() -> list:
        """Get all messages"""
        return st.session_state.get("messages", [])
    
    @staticmethod
    def cache_vision_result(image_hash: str, text: str, info: Dict):
        """Cache vision API result"""
        if "vision_cache" not in st.session_state:
            st.session_state.vision_cache = {}
        st.session_state.vision_cache[image_hash] = {
            "text": text,
            "info": info
        }
    
    @staticmethod
    def get_cached_vision_result(image_hash: str) -> Optional[Dict]:
        """Get cached vision API result"""
        cache = st.session_state.get("vision_cache", {})
        return cache.get(image_hash)
    
    @staticmethod
    def is_image_processed(image_hash: str) -> bool:
        """Check if image has already been processed"""
        processed = st.session_state.get("processed_images", set())
        return image_hash in processed
    
    @staticmethod
    def mark_image_processed(image_hash: str):
        """Mark image as processed"""
        if "processed_images" not in st.session_state:
            st.session_state.processed_images = set()
        st.session_state.processed_images.add(image_hash)
    
    @staticmethod
    def get_common_issues() -> list:
        """Get common issues list"""
        return st.session_state.get("common_issues", [])
    
    @staticmethod
    def set_common_issues(issues: list):
        """Set common issues list"""
        st.session_state.common_issues = issues
    
    @staticmethod
    def get_issue_summary() -> str:
        """Get issue summary"""
        return st.session_state.get("issue_summary", "")
    
    @staticmethod
    def set_issue_summary(summary: str):
        """Set issue summary"""
        st.session_state.issue_summary = summary

