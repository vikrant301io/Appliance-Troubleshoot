"""Main Streamlit application with new flow structure using LangChain"""
import streamlit as st
from typing import Optional, List, Dict
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
BASE_DIR = Path(__file__).parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

from config import PAGE_TITLE, PAGE_ICON, OPENAI_API_KEY
from app.models.appliance import Appliance
from app.models.booking import Booking, TimeSlot, CostBreakdown
from app.models.technician import Technician
from app.models.problem import Part
from app.repositories.knowledge_base_repository import KnowledgeBaseRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.technician_repository import TechnicianRepository
from app.repositories.common_issues_repository import CommonIssuesRepository
from app.services.openai_service import OpenAIService
from app.services.appliance_service import ApplianceService
from app.services.flow_orchestrator import FlowOrchestrator
from app.services.booking_service import BookingService
from app.utils.state_manager import StateManager
from app.utils.image_utils import ImageUtils
from app.utils.parts_loader import PartsLoader
from components.technician_booking import (
    display_technician_list,
    display_time_slot_selector,
    display_payment_options,
    display_booking_summary
)
from components.landing_page import (
    render_landing_page,
    render_manual_input_form,
    render_product_label_help
)
from components.category_selection import render_category_selection


class ApplianceTroubleshootApp:
    """Main application class with new flow structure"""
    
    def __init__(self):
        """Initialize application with dependencies"""
        # Initialize repositories
        self.knowledge_base_repo = KnowledgeBaseRepository()
        self.booking_repo = BookingRepository()
        self.technician_repo = TechnicianRepository()
        self.common_issues_repo = CommonIssuesRepository()
        
        # Initialize services
        try:
            self.openai_service = OpenAIService()
            self.appliance_service = ApplianceService(self.openai_service)
            self.flow_orchestrator = FlowOrchestrator()
        except ValueError:
            self.openai_service = None
            self.appliance_service = None
            self.flow_orchestrator = None
        
        self.booking_service = BookingService(self.knowledge_base_repo)
        
        # Initialize state
        StateManager.initialize()
    
    def run(self):
        """Run the Streamlit application"""
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        
        # Add CSS for issue buttons
        st.markdown("""
        <style>
        /* Style issue buttons to look like clickable boxes */
        button[key^="issue_btn_"] {
            background-color: #f0f0f0 !important;
            color: #000 !important;
            border: 2px solid #2e7d32 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            text-align: left !important;
            transition: all 0.3s !important;
            min-height: 60px !important;
        }
        button[key^="issue_btn_"]:hover {
            background-color: #e8f5e9 !important;
            border-color: #1b5e20 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }
        button[key="describe_issue_btn"] {
            background-color: white !important;
            color: #2e7d32 !important;
            border: 2px solid #2e7d32 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        button[key="describe_issue_btn"]:hover {
            background-color: #f0f0f0 !important;
        }
        button[key="book_tech_btn"] {
            background-color: #2e7d32 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        button[key="book_tech_btn"]:hover {
            background-color: #1b5e20 !important;
        }
        /* Style troubleshoot/book buttons */
        button[key="troubleshoot_btn"] {
            background-color: #2e7d32 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 14px 20px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        button[key="troubleshoot_btn"]:hover {
            background-color: #1b5e20 !important;
        }
        button[key="book_technician_btn"] {
            background-color: white !important;
            color: #2e7d32 !important;
            border: 2px solid #2e7d32 !important;
            border-radius: 8px !important;
            padding: 14px 20px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        button[key="book_technician_btn"]:hover {
            background-color: #e8f5e9 !important;
        }
        /* Style order part buttons */
        button[key^="order_part_"] {
            background-color: #ff9800 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            margin-top: 8px !important;
            margin-bottom: 8px !important;
        }
        button[key^="order_part_"]:hover {
            background-color: #f57c00 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Check API key
        if not self.openai_service or not self.flow_orchestrator:
            st.warning(
                "⚠️ **OpenAI API Key not found!**\n\n"
                "Please set the `OPENAI_API_KEY` environment variable to use this app."
            )
            st.stop()
        
        # Render UI
        self._render_sidebar()
        self._render_main_interface()
    
    def _render_sidebar(self):
        """Render sidebar with controls"""
        with st.sidebar:
            st.title("🔧 Appliance Assistant")
            st.markdown("---")
            
            if st.button("🔄 Start Over", use_container_width=True):
                StateManager.reset()
                if self.flow_orchestrator:
                    self.flow_orchestrator.reset_troubleshooting_memory()
                st.rerun()
            
            st.markdown("---")
            st.markdown("### Current Status")
            st.info(f"**Flow:** {StateManager.get_current_flow()}")
            
            appliance = StateManager.get_appliance()
            if appliance:
                st.markdown("**Appliance:**")
                st.text(f"Type: {appliance.appliance_type or 'Not detected'}")
                st.text(f"Brand: {appliance.brand}")
                st.text(f"Model: {appliance.model}")
    
    def _render_main_interface(self):
        """Render main chat interface"""
        appliance = StateManager.get_appliance()
        messages = StateManager.get_messages()
        current_flow = StateManager.get_current_flow()
        
        # Show category selection first if no category selected
        if current_flow == StateManager.FLOW_CATEGORY_SELECTION:
            selected_category = render_category_selection()
            if selected_category:
                # Store selected category and move to identification flow
                st.session_state.selected_category = selected_category
                StateManager.set_current_flow(StateManager.FLOW_IDENTIFICATION)
                st.rerun()
            return
        
        # Show landing page if no appliance info and no messages yet
        if not appliance and not messages and current_flow == StateManager.FLOW_IDENTIFICATION:
            landing_action = st.session_state.get("landing_action")
            
            if landing_action == "manual" and not st.session_state.get("show_manual_dropdowns", False):
                # Show manual input form (only if dropdowns were not shown on landing page)
                manual_info = render_manual_input_form()
                if manual_info:
                    # Create appliance from manual input
                    appliance = Appliance(
                        brand=manual_info["brand"],
                        model=manual_info["model"],
                        serial=manual_info.get("serial", ""),
                        appliance_type=manual_info.get("appliance_type")
                    )
                    
                    # Detect type if not provided
                    if not appliance.appliance_type and appliance.brand and appliance.model:
                        with st.spinner("Identifying appliance type..."):
                            appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                            if appliance_type:
                                appliance.appliance_type = appliance_type
                    
                    StateManager.set_appliance(appliance)
                    StateManager.add_message("user", f"I entered: Brand: {appliance.brand}, Model: {appliance.model}, Serial: {appliance.serial or 'N/A'}")
                    
                    # For manual input, proceed directly to issue listing without confirmation
                    StateManager.set_current_flow(StateManager.FLOW_ISSUE_LISTING)
                    response = self._get_issue_listing_response()
                    StateManager.add_message("assistant", response)
                    st.session_state.landing_action = None
                    st.rerun()
                return
            elif landing_action == "photo":
                # Show photo upload interface
                st.markdown("### Upload Product Label Photo")
                uploaded_file = st.file_uploader(
                    "Upload a photo of your appliance nameplate",
                    type=["jpg", "jpeg", "png"],
                    help="Upload a clear photo of the label with brand, model, and serial number",
                    key="nameplate_uploader_landing"
                )
                
                if uploaded_file is not None:
                    image_bytes = uploaded_file.read()
                    image_hash = ImageUtils.get_image_hash(image_bytes)
                    
                    if StateManager.is_image_processed(image_hash):
                        return
                    
                    StateManager.mark_image_processed(image_hash)
                    
                    # Process image
                    with st.spinner("Reading nameplate information..."):
                        try:
                            text_content, info = self.appliance_service.identify_from_image(image_bytes)
                            StateManager.cache_vision_result(image_hash, text_content, info)
                        except Exception as e:
                            st.error(f"Error processing image: {e}")
                            return
                    
                    # Create/update appliance
                    appliance = Appliance(brand="", model="")
                    appliance = self.appliance_service.update_appliance_info(appliance, info)
                    
                    # Detect appliance type
                    if appliance.brand and appliance.model:
                        with st.spinner("Identifying appliance type..."):
                            appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                            if appliance_type:
                                appliance.appliance_type = appliance_type
                    
                    StateManager.set_appliance(appliance)
                    StateManager.add_message("user", "I uploaded a nameplate image", image_bytes)
                    
                    # Show detected information with confirm button
                    response = f"""I found the following information from your nameplate:

**Appliance Type:** {appliance.appliance_type or 'Detecting...'}
**Brand:** {appliance.brand}
**Model:** {appliance.model}
**Serial:** {appliance.serial or 'Unknown'}
{f"**Age:** ~{appliance.age} years" if appliance.age else ""}"""
                    
                    StateManager.add_message("assistant", response, image_bytes)
                    st.session_state.landing_action = None
                    st.session_state.show_photo_confirm = True
                    st.rerun()
                
                # Back button
                if st.button("← Back", key="back_from_photo"):
                    st.session_state.landing_action = None
                    st.rerun()
                return
            else:
                # Show landing page (this will show dropdowns if show_manual_dropdowns is True)
                landing_action_result = render_landing_page()
                # If user clicked "Continue to Enter Details" from landing page dropdowns
                if landing_action_result == "manual" and st.session_state.get("show_manual_dropdowns", False):
                    # Now show the manual input form
                    manual_info = render_manual_input_form()
                    if manual_info:
                        # Create appliance from manual input
                        appliance = Appliance(
                            brand=manual_info["brand"],
                            model=manual_info["model"],
                            serial=manual_info.get("serial", ""),
                            appliance_type=manual_info.get("appliance_type")
                        )
                        
                        # Detect type if not provided
                        if not appliance.appliance_type and appliance.brand and appliance.model:
                            with st.spinner("Identifying appliance type..."):
                                appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                                if appliance_type:
                                    appliance.appliance_type = appliance_type
                        
                        StateManager.set_appliance(appliance)
                        StateManager.add_message("user", f"I entered: Brand: {appliance.brand}, Model: {appliance.model}, Serial: {appliance.serial or 'N/A'}")
                        
                        # For manual input, proceed directly to issue listing without confirmation
                        StateManager.set_current_flow(StateManager.FLOW_ISSUE_LISTING)
                        response = self._get_issue_listing_response()
                        StateManager.add_message("assistant", response)
                        st.session_state.landing_action = None
                        st.session_state.show_manual_dropdowns = False
                        st.rerun()
                return
        
        # Regular chat interface
        st.title("🔧 Appliance Troubleshoot Assistant")
        if not messages:
            st.markdown("I'm here to help you fix your appliance or book a technician visit!")
        
        # Display chat messages
        for idx, message in enumerate(messages):
            with st.chat_message(message["role"]):
                content = message["content"]
                st.markdown(content)
                
                # If this is an assistant troubleshooting message
                if message["role"] == "assistant" and StateManager.get_current_flow() == StateManager.FLOW_TROUBLESHOOTING:
                    issue = StateManager.get_problem_description()
                    is_special = issue and PartsLoader.is_special_issue(issue)
                    
                    # Only show API part buttons for non-special issues
                    # For special issues, we show parts selection separately after all messages
                    if not is_special:
                        self._add_order_part_buttons(content, idx)
                
                # Show troubleshoot/book buttons if this is the last message and flag is set
                if (message["role"] == "assistant" and 
                    idx == len(messages) - 1 and 
                    st.session_state.get("show_troubleshoot_book_buttons", False) and
                    "How would you like to proceed" in content):
                    self._show_troubleshoot_book_buttons()
                
                if "image" in message and message["image"]:
                    st.image(message["image"], caption="Uploaded nameplate", width=300)
        
        # After all messages, show parts selection for special issues if in troubleshooting flow
        # CRITICAL: Only show AFTER troubleshooting guidance has been displayed (troubleshooting steps must come first)
        issue = StateManager.get_problem_description()
        
        # Only proceed if we're in troubleshooting flow and troubleshooting has actually started
        troubleshooting_started = st.session_state.get("troubleshooting_started", False)
        
        if (StateManager.get_current_flow() == StateManager.FLOW_TROUBLESHOOTING and
            st.session_state.get("selected_issue_parts") and
            issue and
            PartsLoader.is_special_issue(issue) and
            troubleshooting_started and  # Troubleshooting must have started
            messages and
            len(messages) >= 2):  # At least user message and assistant response
            
            # Check if the last message is troubleshooting guidance with steps
            last_message = messages[-1] if messages else None
            if last_message and last_message.get("role") == "assistant":
                content = last_message.get("content", "")
                
                # CRITICAL CHECK: Verify this is actually troubleshooting guidance with steps
                # Must have Step 1 or Step 2, and NOT be the "how would you like to proceed" message
                # Also ensure it's not a short message (must be actual troubleshooting content)
                has_troubleshooting_steps = (
                    ("Step 1" in content or "Step 2" in content or "Step 3" in content) and
                    "How would you like to proceed" not in content and
                    len(content) > 200  # Ensure it's actual troubleshooting content, not a short message
                )
                
                # Only show parts selection AFTER troubleshooting steps are definitively displayed
                # This ensures troubleshooting steps appear FIRST, then parts selection comes AFTER
                if has_troubleshooting_steps:
                    st.markdown("---")
                    self._show_parts_selection_ui_inline(issue)
        
        # Show confirm button for photo upload if needed
        if st.session_state.get("show_photo_confirm", False):
            appliance = StateManager.get_appliance()
            
            # Check if user wants to edit manually
            if st.session_state.get("show_manual_edit_photo", False):
                # Show manual edit form
                st.markdown("### Edit Model and Serial Number")
                st.info("Please correct the Model Number and Serial Number if they were not detected correctly.")
                
                # Pre-fill with current values
                current_model = appliance.model if appliance else ""
                current_serial = appliance.serial if appliance else ""
                current_brand = appliance.brand if appliance else ""
                current_appliance_type = appliance.appliance_type if appliance else ""
                
                # Show detected brand (read-only)
                if current_brand:
                    st.markdown(f"**Brand:** {current_brand}")
                
                # Manual edit form
                edited_model = st.text_input("Model Number *", value=current_model, key="photo_edit_model")
                edited_serial = st.text_input("Serial Number", value=current_serial, key="photo_edit_serial")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("← Cancel", key="cancel_manual_edit", use_container_width=True):
                        st.session_state.show_manual_edit_photo = False
                        st.rerun()
                
                with col2:
                    if st.button("✓ Save and Continue", key="save_manual_edit", use_container_width=True, type="primary"):
                        if edited_model and edited_model.strip():
                            # Update appliance with edited values
                            appliance.model = edited_model.strip()
                            appliance.serial = edited_serial.strip() if edited_serial else ""
                            
                            # Detect type if not already detected or if model changed
                            if not current_appliance_type or edited_model != current_model:
                                with st.spinner("Identifying appliance type..."):
                                    appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                                    if appliance_type:
                                        appliance.appliance_type = appliance_type
                            
                            StateManager.set_appliance(appliance)
                            
                            # Add a message confirming the edit
                            StateManager.add_message("user", f"I corrected: Model: {appliance.model}, Serial: {appliance.serial or 'N/A'}")
                            updated_response = f"""I've updated the information with your corrections:

**Appliance Type:** {appliance.appliance_type or 'Detecting...'}
**Brand:** {appliance.brand}
**Model:** {appliance.model}
**Serial:** {appliance.serial or 'Unknown'}
{f"**Age:** ~{appliance.age} years" if appliance.age else ""}"""
                            StateManager.add_message("assistant", updated_response)
                            
                            # Move to issue listing
                            StateManager.set_current_flow(StateManager.FLOW_ISSUE_LISTING)
                            st.session_state.show_photo_confirm = False
                            st.session_state.show_manual_edit_photo = False
                            st.session_state.issues_shown = False
                            st.rerun()
                        else:
                            st.error("Model Number is required. Please enter a Model Number.")
            elif appliance and appliance.is_complete():
                # Show two buttons side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✓ Confirm and Continue", key="confirm_photo_details", use_container_width=True, type="primary"):
                        # Detect type if not already detected
                        if not appliance.appliance_type:
                            with st.spinner("Identifying appliance type..."):
                                appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                                if appliance_type:
                                    appliance.appliance_type = appliance_type
                                    StateManager.set_appliance(appliance)
                        
                        # Move to issue listing
                        StateManager.set_current_flow(StateManager.FLOW_ISSUE_LISTING)
                        st.session_state.show_photo_confirm = False
                        st.session_state.issues_shown = False  # Reset to allow _handle_issue_listing_flow to show it
                        st.rerun()
                
                with col2:
                    if st.button("Edit", key="edit_photo_details_manually", use_container_width=True):
                        st.session_state.show_manual_edit_photo = True
                        st.rerun()
        
        # Route to appropriate flow handler
        if current_flow == StateManager.FLOW_IDENTIFICATION:
            self._handle_identification_flow()
        elif current_flow == StateManager.FLOW_ISSUE_LISTING:
            self._handle_issue_listing_flow()
        elif current_flow == StateManager.FLOW_TROUBLESHOOTING:
            self._handle_troubleshooting_flow()
        elif current_flow == StateManager.FLOW_BOOKING:
            self._handle_booking_flow()
        elif current_flow == StateManager.FLOW_PART_ORDERING:
            self._handle_part_ordering_flow()
        
        # Show troubleshoot/book buttons if needed (fallback if not shown in chat message)
        if (st.session_state.get("show_troubleshoot_book_buttons", False) and 
            not any("How would you like to proceed" in msg.get("content", "") for msg in messages if msg.get("role") == "assistant")):
            self._show_troubleshoot_book_buttons()
        
        # Handle text input (if not in booking flow with forms)
        if current_flow != StateManager.FLOW_BOOKING or not st.session_state.get("booking_step") == "technician_selection":
            user_input = st.chat_input("Type your message here...")
            if user_input:
                self._handle_user_input(user_input)
    
    def _handle_identification_flow(self):
        """Handle appliance identification with type detection"""
        appliance = StateManager.get_appliance()
        
        # Show image upload option
        st.markdown("### Upload Product Label Photo")
        uploaded_file = st.file_uploader(
            "Upload a photo of your appliance nameplate",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of the label with brand, model, and serial number",
            key="nameplate_uploader"
        )
        
        if uploaded_file is not None:
            image_bytes = uploaded_file.read()
            image_hash = ImageUtils.get_image_hash(image_bytes)
            
            if StateManager.is_image_processed(image_hash):
                return
            
            StateManager.mark_image_processed(image_hash)
            
            # Process image
            with st.spinner("Reading nameplate information..."):
                try:
                    text_content, info = self.appliance_service.identify_from_image(image_bytes)
                    StateManager.cache_vision_result(image_hash, text_content, info)
                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    return
            
            # Create/update appliance
            if not appliance:
                appliance = Appliance(brand="", model="")
            
            appliance = self.appliance_service.update_appliance_info(appliance, info)
            
            # Detect appliance type
            if appliance.brand and appliance.model:
                with st.spinner("Identifying appliance type..."):
                    appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                    if appliance_type:
                        appliance.appliance_type = appliance_type
            
            StateManager.set_appliance(appliance)
            StateManager.add_message("user", "I uploaded a nameplate image", image_bytes)
            
            # Show detected information with confirm button
            response = f"""I found the following information from your nameplate:

**Appliance Type:** {appliance.appliance_type or 'Detecting...'}
**Brand:** {appliance.brand}
**Model:** {appliance.model}
**Serial:** {appliance.serial or 'Unknown'}
{f"**Age:** ~{appliance.age} years" if appliance.age else ""}"""
            
            StateManager.add_message("assistant", response, image_bytes)
            st.session_state.show_photo_confirm = True
            st.rerun()
        
        # If appliance is complete, ask for confirmation
        if appliance and appliance.is_complete() and not appliance.appliance_type:
            # Detect type if not already detected
            with st.spinner("Identifying appliance type..."):
                appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                if appliance_type:
                    appliance.appliance_type = appliance_type
                    StateManager.set_appliance(appliance)
                    st.rerun()
    
    def _handle_user_input(self, user_input: str):
        """Handle user text input"""
        StateManager.add_message("user", user_input)
        current_flow = StateManager.get_current_flow()
        
        with st.chat_message("assistant"):
            if current_flow == StateManager.FLOW_IDENTIFICATION:
                response = self._process_identification_input(user_input)
            elif current_flow == StateManager.FLOW_ISSUE_LISTING:
                response = self._process_issue_listing_input(user_input)
            elif current_flow == StateManager.FLOW_TROUBLESHOOTING:
                response = self._process_troubleshooting_input(user_input)
            else:
                response = "I'm not sure how to help with that. Could you rephrase?"
            
            st.markdown(response)
        
        StateManager.add_message("assistant", response)
        st.rerun()
    
    def _process_identification_input(self, user_input: str) -> str:
        """Process input during identification flow"""
        appliance = StateManager.get_appliance()
        if not appliance:
            appliance = Appliance(brand="", model="")
        
        # Check if user is confirming
        if appliance.is_complete():
            if any(kw in user_input.lower() for kw in ["yes", "correct", "right", "confirm"]):
                # Detect type if not already detected
                if not appliance.appliance_type:
                    appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                    if appliance_type:
                        appliance.appliance_type = appliance_type
                        StateManager.set_appliance(appliance)
                
                # Move to issue listing
                StateManager.set_current_flow(StateManager.FLOW_ISSUE_LISTING)
                return self._get_issue_listing_response()
        
        # Extract appliance info from text
        info = self.appliance_service.identify_from_text(user_input)
        if info:
            appliance = self.appliance_service.update_appliance_info(appliance, info)
            StateManager.set_appliance(appliance)
            
            # Detect type if we have brand and model
            if appliance.is_complete() and not appliance.appliance_type:
                appliance_type = self.flow_orchestrator.detect_appliance_type(appliance)
                if appliance_type:
                    appliance.appliance_type = appliance_type
                    StateManager.set_appliance(appliance)
        
        # Check if we have enough info
        if appliance.is_complete():
            return f"""I have:

**Appliance Type:** {appliance.appliance_type or 'Detecting...'}
**Brand:** {appliance.brand}
**Model:** {appliance.model}
**Serial:** {appliance.serial or 'Unknown'}

Does this look correct? Please confirm."""
        else:
            return "I need a bit more information. Please provide:\n- Brand (e.g., Samsung, LG)\n- Model number\n- Serial number (if available)\n\nOr upload a photo of the nameplate!"
    
    def _get_issue_listing_response(self) -> str:
        """Get response for issue listing flow"""
        appliance = StateManager.get_appliance()
        if not appliance or not appliance.appliance_type:
            return "I need to identify your appliance first. Please provide brand, model, and serial number."
        
        # Get common issues from repository first, then enhance with agent
        common_issues = self.common_issues_repo.get_issues_for_type(appliance.appliance_type)
        
        # Enhance with LangChain agent if available
        if self.flow_orchestrator:
            agent_issues = self.flow_orchestrator.list_common_issues(appliance)
            if agent_issues:
                # Merge and deduplicate
                all_issues = list(set(common_issues + agent_issues))
                common_issues = all_issues
        
        # For Refrigerators, ensure specific required issues are always included
        if appliance.appliance_type == "Refrigerator":
            required_issues = [
                "Lights Not Working Inside",
                "Water Leakage Inside / Outside",
                "Door Not Sealing Properly"
            ]
            
            # Patterns to identify similar issues that should be removed (case-insensitive)
            patterns_to_remove = [
                r"light.*not.*(?:working|turning|on|off)",  # Matches "light not turning on", "lights not working", etc.
                r"(?:lights?|lamp|bulb).*not.*working",    # Matches "lights not working", "bulb not working"
                r"water.*leak",                            # Matches "water leakage", "water leak", "water leaking"
                r"leakage.*water",                         # Matches "leakage inside", "water leakage"
                r"door.*(?:not.*)?seal",                   # Matches "door not sealing", "door sealing", "door seal"
                r"seal.*door"                              # Matches "sealing properly" in context of door
            ]
            
            import re
            
            # Remove similar issues from common_issues (case-insensitive matching)
            filtered_issues = []
            for issue in common_issues:
                issue_lower = issue.lower()
                # Check if this issue matches any pattern
                should_remove = False
                for pattern in patterns_to_remove:
                    if re.search(pattern, issue_lower):
                        should_remove = True
                        break
                
                if not should_remove:
                    filtered_issues.append(issue)
            
            # Start with required issues, then add other issues
            final_issues = required_issues + filtered_issues
            # Limit to 10 total issues
            common_issues = final_issues[:10]
        
        # Limit to 10 if not Refrigerator
        if appliance.appliance_type != "Refrigerator":
            common_issues = common_issues[:10]
        
        StateManager.set_common_issues(common_issues)
        
        if common_issues:
            return f"""Great! I've identified your {appliance.appliance_type}.

Here are some common issues with {appliance.appliance_type}s:"""
        else:
            return f"""Great! I've identified your {appliance.appliance_type}.

What problem are you experiencing with your {appliance.appliance_type}?"""
    
    def _handle_issue_listing_flow(self):
        """Handle issue listing flow - show common issues as clickable buttons"""
        if not st.session_state.get("issues_shown"):
            appliance = StateManager.get_appliance()
            if appliance and appliance.appliance_type:
                response = self._get_issue_listing_response()
                StateManager.add_message("assistant", response)
                st.session_state.issues_shown = True
                st.rerun()
        
        # Check if an issue has already been selected
        existing_problem = StateManager.get_problem_description()
        
        # Only show issue buttons if no issue has been selected yet
        if not existing_problem:
            # Display clickable issue buttons
            common_issues = StateManager.get_common_issues()
            if common_issues:
                st.markdown("### Select an Issue:")
                
                # Display issues in a grid of clickable buttons
                cols_per_row = 2
                for i in range(0, len(common_issues), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(common_issues):
                            issue = common_issues[i + j]
                            with col:
                                if st.button(issue, key=f"issue_btn_{i+j}", use_container_width=True):
                                    StateManager.set_problem_description(issue)
                                    StateManager.add_message("user", issue)
                                    
                                    # Check if this is a special issue with parts and store for later
                                    if PartsLoader.is_special_issue(issue):
                                        parts = PartsLoader.load_parts_for_issue(issue, BASE_DIR)
                                        if parts:
                                            st.session_state.selected_issue_parts = parts
                                            st.session_state.special_issue_name = issue
                                    
                                    # Always go through normal troubleshoot/book flow first
                                    response = self._ask_troubleshoot_or_book(issue)
                                    StateManager.add_message("assistant", response)
                                    st.rerun()
                
                st.markdown("---")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📝 Describe Issue Directly", key="describe_issue_btn", use_container_width=True):
                        st.session_state.show_issue_input = True
                        st.rerun()
                
                with col2:
                    if st.button("🔧 Book a Technician", key="book_tech_btn", use_container_width=True, type="primary"):
                        StateManager.set_current_flow(StateManager.FLOW_BOOKING)
                        response = self._start_booking_flow()
                        StateManager.add_message("assistant", response)
                        st.rerun()
            
            # Show text input if user clicked "Describe Issue Directly"
            if st.session_state.get("show_issue_input", False):
                user_issue = st.text_input("Describe your issue:", key="custom_issue_input", placeholder="e.g., My refrigerator is making loud noises")
                if user_issue:
                    StateManager.set_problem_description(user_issue)
                    StateManager.add_message("user", user_issue)
                    
                    # Check if this is a special issue with parts and store for later
                    if PartsLoader.is_special_issue(user_issue):
                        parts = PartsLoader.load_parts_for_issue(user_issue, BASE_DIR)
                        if parts:
                            st.session_state.selected_issue_parts = parts
                            st.session_state.special_issue_name = user_issue
                    
                    # Always go through normal troubleshoot/book flow first
                    response = self._ask_troubleshoot_or_book(user_issue)
                    StateManager.add_message("assistant", response)
                    st.session_state.show_issue_input = False
                    st.rerun()
    
    def _process_issue_listing_input(self, user_input: str) -> str:
        """Process input during issue listing flow"""
        # Check if we already have a problem description (user has selected an issue)
        existing_problem = StateManager.get_problem_description()
        
        # If problem already exists, check if user is choosing troubleshoot or book
        if existing_problem:
            # Check if user wants to troubleshoot
            if any(kw in user_input.lower() for kw in ["1", "troubleshoot", "self", "guide", "fix", "repair myself"]):
                StateManager.set_current_flow(StateManager.FLOW_TROUBLESHOOTING)
                st.session_state.troubleshooting_started = True
                
                # Get initial troubleshooting guidance
                appliance = StateManager.get_appliance()
                issue = existing_problem
                guidance = self.flow_orchestrator.get_troubleshooting_guidance(
                    appliance=appliance,
                    issue=issue,
                    conversation_history=[]
                )
                return guidance
            
            # Check if user wants to book technician
            elif any(kw in user_input.lower() for kw in ["2", "book", "technician", "repair", "schedule", "professional"]):
                StateManager.set_current_flow(StateManager.FLOW_BOOKING)
                return self._start_booking_flow()
        
        # Check if user wants to book technician (before selecting issue)
        if any(kw in user_input.lower() for kw in ["book", "technician", "repair", "schedule"]):
            StateManager.set_current_flow(StateManager.FLOW_BOOKING)
            return self._start_booking_flow()
        
        # Check if user selected a number from the list
        common_issues = StateManager.get_common_issues()
        if common_issues:
            try:
                # Try to parse as number
                issue_num = int(user_input.strip())
                if 1 <= issue_num <= len(common_issues):
                    selected_issue = common_issues[issue_num - 1]
                    StateManager.set_problem_description(selected_issue)
                    return self._ask_troubleshoot_or_book(selected_issue)
            except ValueError:
                pass
        
        # User described their issue
        StateManager.set_problem_description(user_input)
        return self._ask_troubleshoot_or_book(user_input)
    
    def _show_parts_selection_ui(self, issue: str):
        """Show parts selection UI for special issues with part images"""
        parts = st.session_state.get("selected_issue_parts", [])
        
        if not parts:
            st.error("No parts found for this issue.")
            return
        
        st.markdown("### Select Parts to Order")
        st.markdown(f"**Issue:** {issue}")
        st.markdown(f"**Available Parts:** {len(parts)}")
        st.markdown("---")
        
        # Initialize selected parts in session state if not exists
        if "selected_parts_indices" not in st.session_state:
            st.session_state.selected_parts_indices = []
        
        # Display parts in a grid with images
        cols_per_row = 2
        checkbox_states = {}  # Track checkbox states
        
        for i in range(0, len(parts), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(parts):
                    part = parts[i + j]
                    part_idx = i + j
                    
                    with col:
                        # Create a container for each part
                        with st.container():
                            # Display part image first (so it's visible)
                            try:
                                from PIL import Image
                                img = Image.open(part['image_path'])
                                st.image(img, caption=part['name'], use_container_width=True)
                            except Exception as e:
                                st.error(f"Could not load image: {e}")
                            
                            # Display part details
                            st.markdown(f"**{part['name']}**")
                            st.markdown(f"**Price:** ${part['price']:.2f}")
                            
                            # Checkbox for selection (placed after image and details)
                            checkbox_key = f"part_checkbox_{part_idx}"
                            is_selected = st.checkbox(
                                "Select this part",
                                value=part_idx in st.session_state.selected_parts_indices,
                                key=checkbox_key
                            )
                            checkbox_states[part_idx] = is_selected
                            
                            st.markdown("---")
        
        # Update selection list after all checkboxes are rendered
        st.session_state.selected_parts_indices = [idx for idx, checked in checkbox_states.items() if checked]
        
        # Calculate total
        selected_parts = [parts[i] for i in st.session_state.selected_parts_indices]
        total_price = sum(p['price'] for p in selected_parts)
        
        if selected_parts:
            st.markdown("### Selected Parts Summary")
            for part in selected_parts:
                st.markdown(f"- **{part['name']}** - ${part['price']:.2f}")
            st.markdown(f"**Total:** ${total_price:.2f}")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Skip Parts & Troubleshoot", key="skip_parts_troubleshoot", use_container_width=True):
                st.session_state.show_parts_selection = False
                st.session_state.selected_parts_indices = []
                response = self._ask_troubleshoot_or_book(issue)
                StateManager.add_message("assistant", response)
                st.rerun()
        
        with col2:
            button_enabled = len(selected_parts) > 0
            if st.button("📦 Order Part Confirm", key="order_part_confirm_from_selection", use_container_width=True, type="primary", disabled=not button_enabled):
                if selected_parts:
                    # Store selected parts for ordering
                    appliance = StateManager.get_appliance()
                    selected_parts_data = []
                    for part in selected_parts:
                        selected_parts_data.append({
                            "name": part['name'],
                            "part_number": part['name'],  # Using name as part number for now
                            "price": part['price'],
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": part.get('image_path')
                        })
                    
                    # Store all selected parts - if multiple parts, combine them
                    if len(selected_parts_data) == 1:
                        st.session_state.current_order_part = selected_parts_data[0]
                    else:
                        # For multiple parts, combine them into a single order entry
                        total_price = sum(p['price'] for p in selected_parts_data)
                        combined_names = " + ".join([p['name'] for p in selected_parts_data])
                        st.session_state.current_order_part = {
                            "name": combined_names,
                            "part_number": "Multiple Parts",
                            "price": total_price,
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": selected_parts_data[0].get('image_path'),  # Show first image
                            "all_parts": selected_parts_data  # Store all parts for reference
                        }
                    
                    # Initialize part ordering flow
                    StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                    st.session_state.order_step = "address_confirmation"
                    st.session_state.show_parts_selection = False
                    st.session_state.selected_parts_indices = []
                    
                    parts_list = ", ".join([p['name'] for p in selected_parts])
                    StateManager.add_message("user", f"I want to order: {parts_list}")
                    StateManager.add_message("assistant", f"Excellent! I'll help you order **{parts_list}**. Let's proceed with your order details.")
                    st.rerun()
                else:
                    st.warning("Please select at least one part to order.")
    
    def _show_parts_selection_ui_inline(self, issue: str):
        """Show parts selection UI inline after troubleshooting guidance"""
        parts = st.session_state.get("selected_issue_parts", [])
        
        if not parts:
            return
        
        st.markdown("### 📦 Select Parts to Order")
        st.markdown(f"**Available Parts for {issue}:** {len(parts)}")
        st.markdown("---")
        
        # Initialize selected parts in session state if not exists
        if "selected_parts_indices_inline" not in st.session_state:
            st.session_state.selected_parts_indices_inline = []
        
        # Display parts in a grid with images
        cols_per_row = 2
        checkbox_states = {}  # Track checkbox states
        
        for i in range(0, len(parts), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(parts):
                    part = parts[i + j]
                    part_idx = i + j
                    
                    with col:
                        # Create a container for each part
                        with st.container():
                            # Display part image first (so it's visible)
                            try:
                                from PIL import Image
                                img = Image.open(part['image_path'])
                                st.image(img, caption=part['name'], use_container_width=True)
                            except Exception as e:
                                st.error(f"Could not load image: {e}")
                            
                            # Display part details
                            st.markdown(f"**{part['name']}**")
                            st.markdown(f"**Price:** ${part['price']:.2f}")
                            
                            # Checkbox for selection (placed after image and details)
                            checkbox_key = f"inline_part_checkbox_{part_idx}"
                            is_selected = st.checkbox(
                                "Select this part",
                                value=part_idx in st.session_state.selected_parts_indices_inline,
                                key=checkbox_key
                            )
                            checkbox_states[part_idx] = is_selected
                            
                            st.markdown("---")
        
        # Update selection list after all checkboxes are rendered
        st.session_state.selected_parts_indices_inline = [idx for idx, checked in checkbox_states.items() if checked]
        
        # Calculate total
        selected_parts = [parts[i] for i in st.session_state.selected_parts_indices_inline]
        total_price = sum(p['price'] for p in selected_parts)
        
        if selected_parts:
            st.markdown("### Selected Parts Summary")
            for part in selected_parts:
                st.markdown(f"- **{part['name']}** - ${part['price']:.2f}")
            st.markdown(f"**Total:** ${total_price:.2f}")
        
        st.markdown("---")
        
        # Action buttons - two options: Order Parts only, or Order Parts + Book Technician
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📦 Order Selected Parts", key="order_selected_parts_inline", use_container_width=True, type="primary", disabled=len(selected_parts) == 0):
                if selected_parts:
                    # Store selected parts for ordering
                    appliance = StateManager.get_appliance()
                    selected_parts_data = []
                    for part in selected_parts:
                        selected_parts_data.append({
                            "name": part['name'],
                            "part_number": part['name'],  # Using name as part number for now
                            "price": part['price'],
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": part.get('image_path')
                        })
                    
                    # Store all selected parts - if multiple parts, combine them
                    if len(selected_parts_data) == 1:
                        st.session_state.current_order_part = selected_parts_data[0]
                    else:
                        # For multiple parts, combine them into a single order entry
                        total_price = sum(p['price'] for p in selected_parts_data)
                        combined_names = " + ".join([p['name'] for p in selected_parts_data])
                        st.session_state.current_order_part = {
                            "name": combined_names,
                            "part_number": "Multiple Parts",
                            "price": total_price,
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": selected_parts_data[0].get('image_path'),  # Show first image
                            "all_parts": selected_parts_data  # Store all parts for reference
                        }
                    
                    # Initialize part ordering flow
                    StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                    st.session_state.order_step = "address_confirmation"
                    st.session_state.selected_parts_indices_inline = []
                    
                    parts_list = ", ".join([p['name'] for p in selected_parts])
                    StateManager.add_message("user", f"I want to order: {parts_list}")
                    StateManager.add_message("assistant", f"Excellent! I'll help you order **{parts_list}**. Let's proceed with your order details.")
                    st.rerun()
                else:
                    st.warning("Please select at least one part to order.")
        
        with col2:
            if st.button("📦 Order Parts + Book Technician", key="order_parts_book_tech_inline", use_container_width=True, disabled=len(selected_parts) == 0):
                if selected_parts:
                    # Store selected parts for ordering
                    appliance = StateManager.get_appliance()
                    selected_parts_data = []
                    for part in selected_parts:
                        selected_parts_data.append({
                            "name": part['name'],
                            "part_number": part['name'],  # Using name as part number for now
                            "price": part['price'],
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": part.get('image_path')
                        })
                    
                    # Store all selected parts - if multiple parts, combine them
                    if len(selected_parts_data) == 1:
                        st.session_state.current_order_part = selected_parts_data[0]
                    else:
                        # For multiple parts, combine them into a single order entry
                        total_price = sum(p['price'] for p in selected_parts_data)
                        combined_names = " + ".join([p['name'] for p in selected_parts_data])
                        st.session_state.current_order_part = {
                            "name": combined_names,
                            "part_number": "Multiple Parts",
                            "price": total_price,
                            "appliance_type": appliance.appliance_type if appliance else None,
                            "brand": appliance.brand if appliance else None,
                            "model": appliance.model if appliance else None,
                            "image_path": selected_parts_data[0].get('image_path'),  # Show first image
                            "all_parts": selected_parts_data  # Store all parts for reference
                        }
                    
                    # Mark as combined flow (order + booking)
                    st.session_state.combined_order_booking = True
                    
                    # Initialize part ordering flow first
                    StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                    st.session_state.order_step = "address_confirmation"
                    st.session_state.selected_parts_indices_inline = []
                    
                    parts_list = ", ".join([p['name'] for p in selected_parts])
                    StateManager.add_message("user", f"I want to order: {parts_list} and book a technician")
                    StateManager.add_message("assistant", f"Perfect! I'll help you order **{parts_list}** and book a technician. Let's start with your order details.")
                    st.rerun()
                else:
                    st.warning("Please select at least one part to order.")
    
    def _ask_troubleshoot_or_book(self, issue: str) -> str:
        """Ask user if they want to troubleshoot or book technician"""
        # Set flag to show action buttons
        st.session_state.show_troubleshoot_book_buttons = True
        return f"""I understand you're experiencing: **{issue}**

How would you like to proceed?"""
    
    def _add_order_part_buttons(self, content: str, message_idx: int):
        """Add order part buttons when a specific part is identified in the troubleshooting response"""
        import re
        
        # Extract ALL parts from the content (handle multiple parts)
        parts = []
        
        # Split content by "Part Required:" to find all part blocks
        part_sections = re.split(r'(?:\*\*)?Part Required(?:\*\*)?:', content, flags=re.IGNORECASE)
        
        # Process each section (skip the first one as it's before any "Part Required:")
        for i in range(1, len(part_sections)):
            section = part_sections[i]
            
            # Extract part name (first line after "Part Required:")
            lines = [line.strip() for line in section.split('\n') if line.strip()]
            part_name = lines[0] if lines else None
            # Clean up part name - remove any markdown formatting
            if part_name:
                part_name = re.sub(r'\*\*', '', part_name).strip()
            
            # Look for Part Number and Cost in this section (more flexible patterns)
            part_num_match = re.search(r'(?:\*\*)?Part Number(?:\*\*)?[:\s]+([^\n]+)', section, re.IGNORECASE)
            
            part_number = part_num_match.group(1).strip() if part_num_match else None
            if part_number:
                # Clean up markdown formatting
                part_number = re.sub(r'\*\*', '', part_number).strip()
            
            # Try multiple cost patterns - comprehensive search
            part_cost = None
            cost_patterns = [
                r'\*\*Cost\*\*[:\s]+\$?\s*([\d.]+)',  # **Cost:** $150
                r'(?:\*\*)?Cost(?:\*\*)?[:\s]+\$?\s*([\d.]+)',  # Cost: $150 or Cost: 150
                r'Cost[:\s]+\$([\d.]+)',  # Cost: $150
                r'Cost[:\s]+([\d.]+)',  # Cost: 150
                r'\$\s*([\d.]+)',  # Just $150 (anywhere in section)
            ]
            
            # First try in the section
            for pattern in cost_patterns:
                part_cost_match = re.search(pattern, section, re.IGNORECASE)
                if part_cost_match:
                    try:
                        cost_str = part_cost_match.group(1).strip()
                        part_cost = float(cost_str)
                        if part_cost > 0:  # Valid cost found
                            break
                    except (ValueError, AttributeError):
                        continue
            
            # If not found in section, try in the full content near the part number
            if not part_cost and part_number:
                # Look for cost near the part number (within 300 chars)
                part_num_pos = content.find(part_number)
                if part_num_pos != -1:
                    nearby_text = content[max(0, part_num_pos-150):part_num_pos+300]
                    for pattern in cost_patterns:
                        part_cost_match = re.search(pattern, nearby_text, re.IGNORECASE)
                        if part_cost_match:
                            try:
                                cost_str = part_cost_match.group(1).strip()
                                part_cost = float(cost_str)
                                if part_cost > 0:
                                    break
                            except (ValueError, AttributeError):
                                continue
                    
                    # Last resort: find any dollar amount in nearby text
                    if not part_cost:
                        dollar_matches = re.findall(r'\$(\d+(?:\.\d{2})?)', nearby_text)
                        for amt_str in dollar_matches:
                            try:
                                amt = float(amt_str)
                                if 1 <= amt <= 10000:  # Reasonable range
                                    part_cost = amt
                                    break
                            except ValueError:
                                continue
            
            # Allow part to be added even if cost is missing (we'll try to extract it later)
            if part_name and part_number:
                parts.append({
                    "name": part_name,
                    "part_number": part_number,
                    "price": part_cost if part_cost and part_cost > 0 else 0.0  # Default to 0.0 if not found
                })
        
        # If no parts found with the block pattern, try the old single-part method
        if not parts:
            part_name = None
            part_number = None
            part_cost = None
            
            # Look for Part Required (more flexible pattern)
            part_name_pattern = r'(?:\*\*)?Part Required(?:\*\*)?[:\s]+([^\n]+)'
            part_name_match = re.search(part_name_pattern, content, re.IGNORECASE)
            if part_name_match:
                part_name = part_name_match.group(1).strip()
                # Clean up markdown formatting
                part_name = re.sub(r'\*\*', '', part_name).strip()
            
            # Look for Part Number (more flexible pattern)
            part_num_pattern = r'(?:\*\*)?Part Number(?:\*\*)?[:\s]+([^\n]+)'
            part_num_match = re.search(part_num_pattern, content, re.IGNORECASE)
            if part_num_match:
                part_number = part_num_match.group(1).strip()
                # Clean up markdown formatting
                part_number = re.sub(r'\*\*', '', part_number).strip()
            
            # Try multiple cost patterns - search in full content
            part_cost = None
            cost_patterns = [
                r'(?:\*\*)?Cost(?:\*\*)?[:\s]+\$?\s*([\d.]+)',  # Cost: $150 or Cost: 150
                r'Cost[:\s]+\$([\d.]+)',  # Cost: $150
                r'Cost[:\s]+([\d.]+)',  # Cost: 150
            ]
            
            # Try in full content
            for pattern in cost_patterns:
                part_cost_match = re.search(pattern, content, re.IGNORECASE)
                if part_cost_match:
                    try:
                        cost_str = part_cost_match.group(1).strip()
                        part_cost = float(cost_str)
                        if part_cost > 0:  # Valid cost found
                            break
                    except (ValueError, AttributeError):
                        continue
            
            # If still not found and we have part number, look near it
            if not part_cost and part_number:
                part_num_pos = content.find(part_number)
                if part_num_pos != -1:
                    nearby_text = content[max(0, part_num_pos-100):part_num_pos+200]
                    for pattern in cost_patterns:
                        part_cost_match = re.search(pattern, nearby_text, re.IGNORECASE)
                        if part_cost_match:
                            try:
                                cost_str = part_cost_match.group(1).strip()
                                part_cost = float(cost_str)
                                if part_cost > 0:
                                    break
                            except (ValueError, AttributeError):
                                continue
            
            # Allow part to be added even if cost is missing (we'll try to extract it later)
            if part_name and part_number:
                parts.append({
                    "name": part_name,
                    "part_number": part_number,
                    "price": part_cost if part_cost and part_cost > 0 else 0.0  # Default to 0.0 if not found
                })
        
        # Check for the text pattern about ordering the part
        order_text_patterns = [
            r'If you want to order the part',
            r'Would you like assistance.*?ordering.*?part',
            r'order the part.*?book.*?technician',
            r'order.*?technician.*?bring.*?install'
        ]
        has_order_text = any(re.search(pattern, content, re.IGNORECASE | re.DOTALL) for pattern in order_text_patterns)
        
        # Show buttons if we have parts OR the order text pattern
        should_show_buttons = len(parts) > 0 or has_order_text
        
        if should_show_buttons:
            st.markdown("---")
            
            # If multiple parts, show selection first
            selected_part = None
            if len(parts) > 1:
                st.markdown("**Please select which part you would like to order:**")
                selected_part_idx = st.radio(
                    "Select Part",
                    options=range(len(parts)),
                    format_func=lambda i: f"{parts[i]['name']} (Part #: {parts[i]['part_number']}, Cost: ${parts[i]['price']:.2f})",
                    key=f"part_selection_{message_idx}"
                )
                selected_part = parts[selected_part_idx]
            elif len(parts) == 1:
                selected_part = parts[0]
            
            # Show buttons if we have a selected part OR if we have order text (fallback)
            if selected_part or has_order_text:
                col1, col2 = st.columns(2)
                
                with col1:
                    button_key = f"order_part_confirm_{message_idx}"
                    if st.button("📦 Order Part Confirm", key=button_key, use_container_width=True, type="primary"):
                        if selected_part:
                            # Store the part info
                            appliance = StateManager.get_appliance()
                            part_price = selected_part["price"]
                            
                            # If price is 0.0, try one more time to extract from content
                            if part_price == 0.0 or part_price is None:
                                # First try standard cost patterns
                                cost_patterns = [
                                    r'(?:\*\*)?Cost(?:\*\*)?[:\s]+\$?\s*([\d.]+)',
                                    r'Cost[:\s]+\$([\d.]+)',
                                    r'Cost[:\s]+([\d.]+)',
                                ]
                                for pattern in cost_patterns:
                                    cost_match = re.search(pattern, content, re.IGNORECASE)
                                    if cost_match:
                                        try:
                                            cost_str = cost_match.group(1).strip()
                                            extracted_cost = float(cost_str)
                                            if extracted_cost > 0:
                                                part_price = extracted_cost
                                                break
                                        except (ValueError, AttributeError):
                                            continue
                                
                                # If still not found, look for any dollar amount near the part number
                                if (part_price == 0.0 or part_price is None) and selected_part.get("part_number"):
                                    part_num = selected_part["part_number"]
                                    part_num_pos = content.find(part_num)
                                    if part_num_pos != -1:
                                        # Look in a 300 character window around the part number
                                        search_window = content[max(0, part_num_pos-150):part_num_pos+300]
                                        # Find all dollar amounts in this window
                                        dollar_amounts = re.findall(r'\$(\d+(?:\.\d{2})?)', search_window)
                                        if dollar_amounts:
                                            # Take the first reasonable dollar amount (between $1 and $10000)
                                            for amt_str in dollar_amounts:
                                                try:
                                                    amt = float(amt_str)
                                                    if 1 <= amt <= 10000:
                                                        part_price = amt
                                                        break
                                                except ValueError:
                                                    continue
                            
                            part_data = {
                                "name": selected_part["name"],
                                "part_number": selected_part["part_number"],
                                "price": part_price if part_price and part_price > 0 else 0.0,
                                "appliance_type": appliance.appliance_type if appliance else None,
                                "brand": appliance.brand if appliance else None,
                                "model": appliance.model if appliance else None
                            }
                            # Store the part to be ordered
                            st.session_state.current_order_part = part_data
                            # Initialize part ordering flow
                            StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                            st.session_state.order_step = "address_confirmation"
                            StateManager.add_message("user", f"I want to order the {selected_part['name']}")
                            StateManager.add_message("assistant", f"Excellent! I'll help you order **{selected_part['name']}** (Part #: {selected_part['part_number']}). Let's proceed with your order details.")
                        else:
                            # Fallback: order text detected but part not parsed - try to extract from content
                            appliance = StateManager.get_appliance()
                            # Try one more time with more lenient extraction
                            fallback_part_name = None
                            fallback_part_number = None
                            fallback_part_cost = None
                            
                            # Try to find part info anywhere in content (more lenient patterns)
                            part_name_match = re.search(r'Part Required[:\s]+([^\n]+)', content, re.IGNORECASE)
                            part_num_match = re.search(r'Part Number[:\s]+([^\n]+)', content, re.IGNORECASE)
                            
                            if part_name_match:
                                fallback_part_name = part_name_match.group(1).strip()
                                # Clean markdown
                                fallback_part_name = re.sub(r'\*\*', '', fallback_part_name).strip()
                            if part_num_match:
                                fallback_part_number = part_num_match.group(1).strip()
                                # Clean markdown
                                fallback_part_number = re.sub(r'\*\*', '', fallback_part_number).strip()
                            
                            # Try multiple cost patterns
                            fallback_part_cost = None
                            cost_patterns = [
                                r'Cost[:\s]+\$?\s*([\d.]+)',  # Cost: $150 or Cost: 150
                                r'Cost[:\s]+\$([\d.]+)',  # Cost: $150
                                r'\$\s*([\d.]+)',  # Just $150
                                r'Cost[:\s]+([\d.]+)',  # Cost: 150
                            ]
                            
                            for pattern in cost_patterns:
                                part_cost_match = re.search(pattern, content, re.IGNORECASE)
                                if part_cost_match:
                                    try:
                                        cost_str = part_cost_match.group(1).strip()
                                        fallback_part_cost = float(cost_str)
                                        if fallback_part_cost > 0:  # Valid cost found
                                            break
                                    except (ValueError, AttributeError):
                                        continue
                            
                            # Create part data even if incomplete
                            part_data = {
                                "name": fallback_part_name or "Replacement Part",
                                "part_number": fallback_part_number or "TBD",
                                "price": fallback_part_cost or 0.0,
                                "appliance_type": appliance.appliance_type if appliance else None,
                                "brand": appliance.brand if appliance else None,
                                "model": appliance.model if appliance else None
                            }
                            st.session_state.current_order_part = part_data
                            StateManager.add_message("user", "I want to order the part")
                            StateManager.add_message("assistant", f"I'll help you order **{part_data['name']}**. Let's proceed with your order details.")
                            st.session_state.order_step = "address_confirmation"
                            StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                        st.rerun()
                
                with col2:
                    button_key2 = f"book_technician_order_part_{message_idx}"
                    if st.button("📦 Book Technician + Order Part", key=button_key2, use_container_width=True):
                        if selected_part:
                            # Store the part info
                            appliance = StateManager.get_appliance()
                            part_data = {
                                "name": selected_part["name"],
                                "part_number": selected_part["part_number"],
                                "price": selected_part["price"],
                                "appliance_type": appliance.appliance_type if appliance else None,
                                "brand": appliance.brand if appliance else None,
                                "model": appliance.model if appliance else None
                            }
                            # Store part and mark as combined flow (order + booking)
                            st.session_state.current_order_part = part_data
                            st.session_state.combined_order_booking = True  # Flag for combined flow
                            # Start with part ordering flow
                            StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                            st.session_state.order_step = "address_confirmation"
                            StateManager.add_message("user", f"I want to order the {selected_part['name']} and book a technician")
                            StateManager.add_message("assistant", f"Perfect! I'll help you order **{selected_part['name']}** (Part #: {selected_part['part_number']}, Cost: ${selected_part['price']:.2f}) and book a technician. Let's start with your order details.")
                        else:
                            # Fallback: order text detected but part not parsed
                            appliance = StateManager.get_appliance()
                            # Try to extract part info from content
                            fallback_part_name = None
                            fallback_part_number = None
                            fallback_part_cost = None
                            
                            part_name_match = re.search(r'Part Required[:\s]+([^\n]+)', content, re.IGNORECASE)
                            part_num_match = re.search(r'Part Number[:\s]+([^\n]+)', content, re.IGNORECASE)
                            part_cost_match = re.search(r'Cost[:\s]+\$?([\d.]+)', content, re.IGNORECASE)
                            
                            if part_name_match:
                                fallback_part_name = re.sub(r'\*\*', '', part_name_match.group(1)).strip()
                            if part_num_match:
                                fallback_part_number = re.sub(r'\*\*', '', part_num_match.group(1)).strip()
                            if part_cost_match:
                                try:
                                    fallback_part_cost = float(part_cost_match.group(1).strip())
                                except ValueError:
                                    pass
                            
                            part_data = {
                                "name": fallback_part_name or "Replacement Part",
                                "part_number": fallback_part_number or "TBD",
                                "price": fallback_part_cost or 0.0,
                                "appliance_type": appliance.appliance_type if appliance else None,
                                "brand": appliance.brand if appliance else None,
                                "model": appliance.model if appliance else None
                            }
                            st.session_state.current_order_part = part_data
                            st.session_state.combined_order_booking = True
                            StateManager.set_current_flow(StateManager.FLOW_PART_ORDERING)
                            st.session_state.order_step = "address_confirmation"
                            StateManager.add_message("user", "I want to order the part and book a technician")
                            StateManager.add_message("assistant", "Perfect! I'll help you order the part and book a technician. Let's start with your order details.")
                        st.rerun()
    
    def _show_troubleshoot_book_buttons(self):
        """Show clickable buttons for troubleshoot or book technician"""
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("DIY", key="troubleshoot_btn", use_container_width=True, type="primary"):
                issue = StateManager.get_problem_description()
                if issue:
                    StateManager.set_current_flow(StateManager.FLOW_TROUBLESHOOTING)
                    st.session_state.show_troubleshoot_book_buttons = False
                    # Reset troubleshooting_started so _handle_troubleshooting_flow can initialize
                    st.session_state.troubleshooting_started = False
                    st.rerun()
        
        with col2:
            if st.button("Book a Technician", key="book_technician_btn", use_container_width=True):
                StateManager.set_current_flow(StateManager.FLOW_BOOKING)
                st.session_state.show_troubleshoot_book_buttons = False
                response = self._start_booking_flow()
                StateManager.add_message("assistant", response)
                st.rerun()
    
    def _process_troubleshooting_input(self, user_input: str) -> str:
        """Process input during troubleshooting flow"""
        # Check if user wants to book technician
        if any(kw in user_input.lower() for kw in ["book", "technician", "repair", "schedule", "stop"]):
            StateManager.set_current_flow(StateManager.FLOW_BOOKING)
            return self._start_booking_flow()
        
        # Continue troubleshooting conversation
        appliance = StateManager.get_appliance()
        issue = StateManager.get_problem_description()
        conversation_history = StateManager.get_messages()
        
        guidance = self.flow_orchestrator.get_troubleshooting_guidance(
            appliance=appliance,
            issue=issue,
            conversation_history=conversation_history
        )
        
        return guidance
    
    def _handle_troubleshooting_flow(self):
        """Handle troubleshooting flow"""
        # If troubleshooting hasn't started yet, initialize it
        if not st.session_state.get("troubleshooting_started"):
            st.session_state.troubleshooting_started = True
            appliance = StateManager.get_appliance()
            issue = StateManager.get_problem_description()
            
            # Reset parts selection shown flag when troubleshooting starts
            # This ensures parts selection will appear AFTER troubleshooting guidance
            st.session_state.parts_selection_shown_after_troubleshooting = False
            
            # Get initial troubleshooting guidance
            guidance = self.flow_orchestrator.get_troubleshooting_guidance(
                appliance=appliance,
                issue=issue,
                conversation_history=[]
            )
            
            StateManager.add_message("assistant", guidance)
            st.rerun()
    
    def _start_booking_flow(self) -> str:
        """Start the booking flow"""
        # Summarize issue
        appliance = StateManager.get_appliance()
        conversation_history = StateManager.get_messages()
        
        issue_summary = self.flow_orchestrator.summarize_issue(
            appliance=appliance,
            conversation_history=conversation_history
        )
        
        StateManager.set_issue_summary(issue_summary)
        st.session_state.booking_step = "technician_selection"
        
        return f"""I'll help you book a technician!

**Issue Summary:** {issue_summary}

Let me show you available technicians..."""
    
    def _handle_booking_flow(self):
        """Handle booking flow with technician selection"""
        booking_step = st.session_state.get("booking_step", "technician_selection")
        appliance = StateManager.get_appliance()
        
        if booking_step == "technician_selection":
            # Show technician list
            technicians = self.technician_repo.get_available_for_appliance(
                appliance.appliance_type or "All Appliances"
            )
            
            if not technicians:
                st.warning("No technicians available for this appliance type.")
                return
            
            selected_id = display_technician_list(technicians)
            
            if selected_id:
                st.session_state.selected_technician_id = selected_id
                st.session_state.booking_step = "time_slot"
                st.rerun()
        
        elif booking_step == "time_slot":
            technician = self.technician_repo.get_by_id(st.session_state.selected_technician_id)
            if not technician:
                st.error("Technician not found.")
                return
            
            time_slot = display_time_slot_selector(technician)
            
            if time_slot:
                st.session_state.time_slot = time_slot
                st.session_state.booking_step = "customer_details"
                st.rerun()
        
        elif booking_step == "customer_details":
            st.markdown("### Customer Information")
            name = st.text_input("Full Name", key="booking_name")
            phone = st.text_input("Phone Number", key="booking_phone")
            address = st.text_area("Address", key="booking_address")
            
            if st.button("Continue", key="continue_booking"):
                if name and phone and address:
                    st.session_state.customer_info = {
                        "name": name,
                        "phone": phone,
                        "address": address
                    }
                    st.session_state.booking_step = "payment"
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
        
        elif booking_step == "payment":
            technician = self.technician_repo.get_by_id(st.session_state.selected_technician_id)
            parts_cost = sum(p.get("price", 0) for p in StateManager.get_suggested_parts())
            total_cost = technician.base_fee + parts_cost
            
            payment_option = display_payment_options(total_cost)
            
            if st.button("Confirm Booking", key="confirm_booking"):
                self._confirm_booking(technician, payment_option, total_cost)
        
        elif booking_step == "confirmed":
            st.success("✅ Booking confirmed! Check the chat for details.")
    
    def _confirm_booking(self, technician: Technician, payment_option: str, total_cost: float):
        """Confirm and save booking"""
        appliance = StateManager.get_appliance()
        time_slot_data = st.session_state.time_slot
        customer_info = st.session_state.customer_info
        issue_summary = StateManager.get_issue_summary()
        
        # Create booking
        booking_id = BookingRepository.generate_booking_id()
        time_slot = TimeSlot(
            date=time_slot_data["date"],
            time=time_slot_data["time"],
            datetime=time_slot_data["datetime"]
        )
        
        parts = [Part.from_dict(p) for p in StateManager.get_suggested_parts()]
        cost = CostBreakdown(
            technician_fee=technician.base_fee,
            parts_total=sum(p.price for p in parts)
        )
        
        booking = Booking(
            booking_id=booking_id,
            timestamp=datetime.now(),
            appliance=appliance,
            problem=issue_summary,
            customer_name=customer_info["name"],
            customer_phone=customer_info["phone"],
            customer_address=customer_info["address"],
            time_slot=time_slot,
            cost=cost,
            technician_id=technician.id,
            technician_name=technician.name,
            payment_option=payment_option,
            payment_status="paid" if payment_option == "pay_now" else "pending"
        )
        
        # Save booking
        self.booking_repo.save(booking)
        st.session_state.booking_step = "confirmed"
        
        # Generate dispatch tracking ID for technician
        dispatch_tracking_id = self._generate_dispatch_tracking_id()
        
        # Show confirmation
        confirmation = f"""✅ **Booking Confirmed!**

**Booking ID:** {booking_id}

**Technician:** {technician.name} (⭐ {technician.rating}/5.0)
**Time Slot:** {time_slot.date} - {time_slot.time}
**Payment:** {'Paid' if payment_option == 'pay_now' else 'Pay on Visit'}
**Total:** ${total_cost:.2f}

**📦 Track Your Dispatch:** [Click here to track your technician dispatch](https://track.example.com/dispatch/{dispatch_tracking_id}) (Dispatch ID: `{dispatch_tracking_id}`)

Your technician will contact you before the visit. Thank you!"""
        
        StateManager.add_message("assistant", confirmation)
        st.rerun()
    
    def _handle_part_ordering_flow(self):
        """Handle part ordering flow with address confirmation, payment, and tracking"""
        import random
        import string
        from datetime import datetime, timedelta
        
        order_step = st.session_state.get("order_step", "address_confirmation")
        part_data = st.session_state.get("current_order_part", {})
        
        if not part_data:
            st.error("No part selected for ordering. Please try again.")
            return
        
        if order_step == "address_confirmation":
            st.markdown("### 📦 Order Confirmation")
            st.markdown("**Part Details:**")
            st.info(f"""
**Part Name:** {part_data.get('name', 'N/A')}
**Part Number:** {part_data.get('part_number', 'N/A')}
**Price:** ${part_data.get('price', 0):.2f}
            """)
            
            st.markdown("---")
            st.markdown("### Delivery Address Confirmation")
            
            # Dummy address data
            default_address = {
                "full_name": "John Doe",
                "street": "123 Main Street",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "phone": "+1 (555) 123-4567",
                "email": "john.doe@example.com"
            }
            
            # Display current address (dummy)
            st.markdown("**Current Address on File:**")
            address_display = f"""
{default_address['full_name']}
{default_address['street']}
{default_address['city']}, {default_address['state']} {default_address['zip_code']}
Phone: {default_address['phone']}
Email: {default_address['email']}
            """
            st.text_area("", value=address_display.strip(), height=100, disabled=True, key="display_address")
            
            # Allow editing
            st.markdown("**Please confirm or update your delivery address:**")
            confirmed_name = st.text_input("Full Name", value=default_address['full_name'], key="order_name")
            confirmed_street = st.text_input("Street Address", value=default_address['street'], key="order_street")
            col1, col2 = st.columns(2)
            with col1:
                confirmed_city = st.text_input("City", value=default_address['city'], key="order_city")
            with col2:
                confirmed_state = st.text_input("State", value=default_address['state'], key="order_state")
            confirmed_zip = st.text_input("ZIP Code", value=default_address['zip_code'], key="order_zip")
            confirmed_phone = st.text_input("Phone Number", value=default_address['phone'], key="order_phone")
            confirmed_email = st.text_input("Email Address", value=default_address['email'], key="order_email")
            
            # Calculate estimated delivery days (dummy logic - 3-7 business days)
            estimated_days = random.randint(3, 7)
            delivery_date = datetime.now() + timedelta(days=estimated_days)
            
            st.markdown("---")
            st.markdown(f"**📅 Estimated Delivery:** {estimated_days} business days")
            st.markdown(f"**Expected Arrival Date:** {delivery_date.strftime('%B %d, %Y')}")
            
            if st.button("✓ Confirm Address & Continue", key="confirm_address_order", type="primary", use_container_width=True):
                # Store confirmed address
                st.session_state.order_address = {
                    "full_name": confirmed_name,
                    "street": confirmed_street,
                    "city": confirmed_city,
                    "state": confirmed_state,
                    "zip_code": confirmed_zip,
                    "phone": confirmed_phone,
                    "email": confirmed_email
                }
                st.session_state.estimated_delivery_days = estimated_days
                st.session_state.expected_delivery_date = delivery_date.strftime('%B %d, %Y')
                
                # Check if this is a combined order+booking flow
                is_combined = st.session_state.get("combined_order_booking", False)
                if is_combined:
                    # For combined flow, skip payment confirmation and go directly to technician selection
                    # Payment will be collected at the final combined confirmation step
                    # Calculate part order total for later use (includes shipping and tax)
                    part_price = part_data.get('price', 0)
                    shipping_cost = 9.99
                    tax = round(part_price * 0.08, 2)  # 8% tax
                    order_total = part_price + shipping_cost + tax
                    
                    # Store individual components for display
                    st.session_state.part_price = part_price
                    st.session_state.shipping_cost = shipping_cost
                    st.session_state.tax = tax
                    
                    # Generate tracking ID
                    tracking_id = self._generate_tracking_id()
                    st.session_state.tracking_id = tracking_id
                    st.session_state.order_total = order_total
                    
                    st.session_state.order_step = "technician_selection"
                else:
                    # Regular order flow - go to payment confirmation
                    st.session_state.order_step = "payment_confirmation"
                st.rerun()
        
        elif order_step == "payment_confirmation":
            st.markdown("### 💳 Payment Information")
            
            # Dummy card details
            default_card = {
                "card_number": "**** **** **** 4532",
                "cardholder_name": "John Doe",
                "expiry_date": "12/25",
                "card_type": "Visa"
            }
            
            st.markdown("**Payment Method on File:**")
            st.info(f"""
**Card Type:** {default_card['card_type']}
**Card Number:** {default_card['card_number']}
**Cardholder Name:** {default_card['cardholder_name']}
**Expiry Date:** {default_card['expiry_date']}
            """)
            
            st.markdown("---")
            st.markdown("**Order Summary:**")
            part_name = part_data.get('name', 'Part')
            part_number = part_data.get('part_number', 'N/A')
            part_price = part_data.get('price', 0)
            shipping_cost = 9.99
            tax = round(part_price * 0.08, 2)  # 8% tax
            total = part_price + shipping_cost + tax
            
            summary_text = f"""
**Part:** {part_name} (Part #: {part_number})
**Part Price:** ${part_price:.2f}
**Shipping:** ${shipping_cost:.2f}
**Tax:** ${tax:.2f}
---
**Total:** ${total:.2f}
            """
            st.markdown(summary_text)
            
            st.markdown("---")
            st.markdown(f"**📅 Expected Delivery:** {st.session_state.get('expected_delivery_date', 'N/A')}")
            
            # Payment confirmation
            st.markdown("**Please confirm your payment details:**")
            confirm_payment = st.checkbox("I confirm that the payment details are correct and authorize this transaction", key="confirm_payment_checkbox")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back to Address", key="back_to_address", use_container_width=True):
                    st.session_state.order_step = "address_confirmation"
                    st.rerun()
            
            with col2:
                # Check if this is a combined order+booking flow
                is_combined = st.session_state.get("combined_order_booking", False)
                button_text = "✓ Confirm Payment & Continue to Technician Booking" if is_combined else "✓ Confirm Payment & Place Order"
                button_key = "confirm_payment_combined" if is_combined else "confirm_payment_order"
                
                if st.button(button_text, key=button_key, type="primary", use_container_width=True, disabled=not confirm_payment):
                    if confirm_payment:
                        # Generate tracking ID
                        tracking_id = self._generate_tracking_id()
                        st.session_state.tracking_id = tracking_id
                        st.session_state.order_total = total
                        
                        if is_combined:
                            # Store order details but don't finalize yet - proceed to technician booking
                            st.session_state.order_step = "technician_selection"
                            st.rerun()
                        else:
                            # Regular order flow - confirm order
                            st.session_state.order_step = "order_confirmed"
                            st.rerun()
                    else:
                        st.warning("Please confirm the payment details checkbox to proceed.")
        
        elif order_step == "technician_selection":
            # Combined flow: After payment, select technician
            st.markdown("### 👨‍🔧 Select Technician")
            st.markdown("**Part Order Summary:**")
            st.info(f"""
**Part:** {part_data.get('name', 'N/A')} (Part #: {part_data.get('part_number', 'N/A')})
**Order Total:** ${st.session_state.get('order_total', 0):.2f}
**Expected Delivery:** {st.session_state.get('expected_delivery_date', 'N/A')}
            """)
            
            st.markdown("---")
            appliance = StateManager.get_appliance()
            technicians = self.technician_repo.get_available_for_appliance(
                appliance.appliance_type or "All Appliances"
            )
            
            if not technicians:
                st.warning("No technicians available for this appliance type.")
                return
            
            selected_id = display_technician_list(technicians)
            
            if selected_id:
                st.session_state.selected_technician_id = selected_id
                st.session_state.order_step = "technician_time_slot"
                st.rerun()
        
        elif order_step == "technician_time_slot":
            # Combined flow: Select time slot (must be after delivery date)
            technician = self.technician_repo.get_by_id(st.session_state.selected_technician_id)
            if not technician:
                st.error("Technician not found.")
                return
            
            # Get delivery date from order
            delivery_date_str = st.session_state.get("expected_delivery_date", "")
            estimated_days = st.session_state.get("estimated_delivery_days", 3)
            
            # Parse delivery date
            try:
                # Parse the formatted date string (e.g., "December 05, 2024")
                delivery_date = datetime.strptime(delivery_date_str, "%B %d, %Y")
            except:
                # Fallback: calculate from estimated days
                from datetime import timedelta
                delivery_date = datetime.now() + timedelta(days=estimated_days)
            
            st.markdown(f"### 📅 Select Technician Time Slot")
            st.info(f"""
**Part Expected Delivery:** {delivery_date_str}

You will be shown 3 available time slots: 1 slot before part arrival (with a warning) and 2 slots after part arrival. We recommend selecting a slot after the part arrives to ensure the technician has the part available for installation.
            """)
            
            # Display time slot selector with date validation
            time_slot = self._display_time_slot_selector_with_validation(technician, delivery_date)
            
            if time_slot:
                # Allow any selected slot (user has been warned if it's before part arrival)
                st.session_state.time_slot = time_slot
                st.session_state.order_step = "combined_confirmation"
                st.rerun()
        
        elif order_step == "combined_confirmation":
            # Combined flow: Final confirmation with order + booking
            technician = self.technician_repo.get_by_id(st.session_state.selected_technician_id)
            if not technician:
                st.error("Technician not found.")
                return
            
            st.markdown("### ✅ Order & Booking Confirmation")
            
            # Order details
            st.markdown("**📦 Part Order Details:**")
            st.info(f"""
**Part:** {part_data.get('name', 'N/A')}
**Part Number:** {part_data.get('part_number', 'N/A')}
**Order Total:** ${st.session_state.get('order_total', 0):.2f}
**Tracking ID:** {st.session_state.get('tracking_id', 'N/A')}
**Expected Delivery:** {st.session_state.get('expected_delivery_date', 'N/A')}
            """)
            
            # Booking details
            st.markdown("**👨‍🔧 Technician Booking Details:**")
            time_slot_data = st.session_state.get("time_slot", {})
            technician_fee_base = 125.00  # Fixed technician fee
            technician_tax = round(technician_fee_base * 0.08, 2)  # 8% tax
            technician_fee_total = technician_fee_base + technician_tax  # Fee with tax
            order_total = st.session_state.get("order_total", 0)
            combined_total = order_total + technician_fee_total
            
            st.info(f"""
**Technician:** {technician.name} (⭐ {technician.rating}/5.0)
**Visit Date:** {time_slot_data.get('date', 'N/A')}
**Visit Time:** {time_slot_data.get('time', 'N/A')}
**Technician Fee:** ${technician_fee_base:.2f}
**Tax:** ${technician_tax:.2f}
**Technician Fee (with Tax):** ${technician_fee_total:.2f}
            """)
            
            # Combined summary with detailed breakdown
            st.markdown("---")
            st.markdown("**💰 Combined Payment Summary:**")
            
            # Get part order breakdown (if stored, otherwise calculate)
            part_price = st.session_state.get("part_price", part_data.get('price', 0))
            shipping_cost = st.session_state.get("shipping_cost", 9.99)
            tax = st.session_state.get("tax", round(part_price * 0.08, 2))
            
            summary_text = f"""
**📦 Part Order Breakdown:**
- Part Price: ${part_price:.2f}
- Shipping: ${shipping_cost:.2f}
- Tax: ${tax:.2f}
- Part Order Subtotal: ${order_total:.2f}

**👨‍🔧 Technician Service:**
- Technician Fee: ${technician_fee_base:.2f}
- Tax: ${technician_tax:.2f}
- Technician Fee (with Tax): ${technician_fee_total:.2f}

---
**💳 Total Amount Due: ${combined_total:.2f}**
            """
            st.markdown(summary_text)
            
            # Payment - Combined payment required (no Pay on Visit option)
            st.markdown("---")
            st.markdown("### 💳 Payment Information")
            
            # Show payment method on file (same as regular payment step)
            default_card = {
                "card_number": "**** **** **** 4532",
                "cardholder_name": "John Doe",
                "expiry_date": "12/25",
                "card_type": "Visa"
            }
            
            st.markdown("**Payment Method on File:**")
            st.info(f"""
**Card Type:** {default_card['card_type']}
**Card Number:** {default_card['card_number']}
**Cardholder Name:** {default_card['cardholder_name']}
**Expiry Date:** {default_card['expiry_date']}
            """)
            
            st.markdown("---")
            st.info(f"**Combined Payment Required:** Both the part order (${order_total:.2f}) and technician fee (${technician_fee_total:.2f}) must be paid together as a single transaction. Total amount due: **${combined_total:.2f}**")
            
            # Payment confirmation checkbox
            confirm_payment = st.checkbox(
                "I authorize the payment of the combined total amount and understand that payment is required at the time of confirmation.",
                key="combined_payment_authorization"
            )
            
            if st.button("✓ Confirm Order & Booking & Proceed to Payment", key="confirm_combined", type="primary", use_container_width=True, disabled=not confirm_payment):
                # Create order record
                order_info = {
                    "tracking_id": st.session_state.get("tracking_id"),
                    "part": part_data,
                    "address": st.session_state.get("order_address", {}),
                    "total": order_total,
                    "delivery_date": st.session_state.get("expected_delivery_date"),
                    "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if "order_history" not in st.session_state:
                    st.session_state.order_history = []
                st.session_state.order_history.append(order_info)
                
                # Calculate technician fee with tax before creating booking
                technician_fee_base = 125.00
                technician_tax = round(technician_fee_base * 0.08, 2)
                technician_fee_with_tax = technician_fee_base + technician_tax
                
                # Create booking record
                appliance = StateManager.get_appliance()
                issue_summary = StateManager.get_issue_summary() or f"Part replacement: {part_data.get('name', 'Part')}"
                customer_info = st.session_state.get("order_address", {})
                
                booking_id = BookingRepository.generate_booking_id()
                time_slot_obj = TimeSlot(
                    date=time_slot_data["date"],
                    time=time_slot_data["time"],
                    datetime=time_slot_data["datetime"]
                )
                
                parts = [Part.from_dict(part_data)]
                cost = CostBreakdown(
                    technician_fee=technician_fee_with_tax,
                    parts_total=part_data.get("price", 0)
                )
                
                booking = Booking(
                    booking_id=booking_id,
                    timestamp=datetime.now(),
                    appliance=appliance,
                    problem=issue_summary,
                    customer_name=customer_info.get("full_name", "N/A"),
                    customer_phone=customer_info.get("phone", "N/A"),
                    customer_address=f"{customer_info.get('street', '')}, {customer_info.get('city', '')}, {customer_info.get('state', '')} {customer_info.get('zip_code', '')}",
                    time_slot=time_slot_obj,
                    cost=cost,
                    technician_id=technician.id,
                    technician_name=technician.name,
                    payment_option="pay_now",  # Always pay now for combined orders
                    payment_status="paid"  # Payment required upfront
                )
                
                self.booking_repo.save(booking)
                
                # Generate dispatch tracking ID for technician
                dispatch_tracking_id = self._generate_dispatch_tracking_id()
                
                # Calculate combined total with technician fee including tax (use values calculated earlier)
                combined_total_with_tax = order_total + technician_fee_with_tax
                
                # Show combined confirmation
                confirmation_message = f"""✅ **Order & Booking Confirmed!**

**📦 Part Order:**
- Part: {part_data.get('name', 'N/A')} (Part #: {part_data.get('part_number', 'N/A')})
- Tracking ID: `{st.session_state.get('tracking_id', 'N/A')}`
- Order Total: ${order_total:.2f}
- Expected Delivery: {st.session_state.get('expected_delivery_date', 'N/A')}

**👨‍🔧 Technician Booking:**
- Booking ID: {booking_id}
- Technician: {technician.name} (⭐ {technician.rating}/5.0)
- Visit Date: {time_slot_data.get('date', 'N/A')} at {time_slot_data.get('time', 'N/A')}
- Technician Fee: ${technician_fee_base:.2f}
- Tax: ${technician_tax:.2f}
- Technician Fee (with Tax): ${technician_fee_with_tax:.2f}
- **📦 Track Your Dispatch:** [Click here to track your technician dispatch](https://track.example.com/dispatch/{dispatch_tracking_id}) (Dispatch ID: `{dispatch_tracking_id}`)

**💰 Combined Total: ${combined_total_with_tax:.2f}**
**Payment Status:** Paid (Combined payment for parts and technician service)

Your part will be delivered first, and the technician will visit on the scheduled date to install it. Thank you!"""
                
                StateManager.add_message("assistant", confirmation_message)
                
                # Reset and return to troubleshooting
                st.session_state.order_step = None
                st.session_state.current_order_part = None
                st.session_state.combined_order_booking = False
                StateManager.set_current_flow(StateManager.FLOW_TROUBLESHOOTING)
                st.rerun()
        
        elif order_step == "order_confirmed":
            tracking_id = st.session_state.get("tracking_id", "N/A")
            order_total = st.session_state.get("order_total", 0)
            delivery_date = st.session_state.get("expected_delivery_date", "N/A")
            
            st.success("✅ **Order Placed Successfully!**")
            
            confirmation_message = f"""
**Order Confirmation**

**Part Ordered:** {part_data.get('name', 'N/A')}
**Part Number:** {part_data.get('part_number', 'N/A')}
**Order Total:** ${order_total:.2f}

**📦 Tracking ID:** `{tracking_id}`

You can use this tracking ID to track your order status. We'll send you email updates at {st.session_state.get('order_address', {}).get('email', 'your email')} as your order progresses.

**Expected Delivery Date:** {delivery_date}

Thank you for your order! If you have any questions, please don't hesitate to contact our support team.
            """
            
            StateManager.add_message("assistant", confirmation_message)
            
            # Store order information
            order_info = {
                "tracking_id": tracking_id,
                "part": part_data,
                "address": st.session_state.get("order_address", {}),
                "total": order_total,
                "delivery_date": delivery_date,
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if "order_history" not in st.session_state:
                st.session_state.order_history = []
            st.session_state.order_history.append(order_info)
            
            # Reset order step and return to troubleshooting
            st.session_state.order_step = None
            st.session_state.current_order_part = None
            StateManager.set_current_flow(StateManager.FLOW_TROUBLESHOOTING)
            st.rerun()
    
    def _display_time_slot_selector_with_validation(self, technician: Technician, part_arrival_date: datetime) -> Optional[dict]:
        """Display time slot selector showing exactly 3 slots: 1 before and 2 after part arrival date"""
        from datetime import timedelta
        
        # Generate exactly 3 time slots
        # 1 slot before part arrival (with warning)
        # 2 slots after part arrival
        
        part_arrival_str = part_arrival_date.strftime('%B %d, %Y')
        today = datetime.now()
        
        # Slot 1: Before part arrival (3 days before)
        before_date = part_arrival_date - timedelta(days=3)
        before_day_name = before_date.strftime("%A")
        
        # Slot 2 & 3: After part arrival (1 day after and 3 days after)
        after_date_1 = part_arrival_date + timedelta(days=1)
        after_date_2 = part_arrival_date + timedelta(days=3)
        after_day_1 = after_date_1.strftime("%A")
        after_day_2 = after_date_2.strftime("%A")
        
        # Build the 3 slots
        slots_to_show = []
        
        # Slot 1: Before part arrival
        for ts in technician.time_slots:
            if ts.day == before_day_name and ts.slots:
                slot_time = ts.slots[0]  # Take first available time
                slots_to_show.append({
                    "date": before_date.strftime("%B %d, %Y"),
                    "day": before_day_name,
                    "time": slot_time,
                    "datetime": before_date,
                    "is_before_arrival": True
                })
                break
        
        # Slot 2: 1 day after part arrival
        for ts in technician.time_slots:
            if ts.day == after_day_1 and ts.slots:
                slot_time = ts.slots[0]
                slots_to_show.append({
                    "date": after_date_1.strftime("%B %d, %Y"),
                    "day": after_day_1,
                    "time": slot_time,
                    "datetime": after_date_1,
                    "is_before_arrival": False
                })
                break
        
        # Slot 3: 3 days after part arrival
        for ts in technician.time_slots:
            if ts.day == after_day_2 and ts.slots:
                slot_time = ts.slots[0]
                slots_to_show.append({
                    "date": after_date_2.strftime("%B %d, %Y"),
                    "day": after_day_2,
                    "time": slot_time,
                    "datetime": after_date_2,
                    "is_before_arrival": False
                })
                break
        
        # If we don't have exact matches, generate fallback slots
        if len(slots_to_show) < 3:
            slots_to_show = []
            
            # Slot 1: Before part arrival (3 days before)
            before_date = part_arrival_date - timedelta(days=3)
            if before_date > today:
                slots_to_show.append({
                    "date": before_date.strftime("%B %d, %Y"),
                    "day": before_date.strftime("%A"),
                    "time": "10:00 AM - 12:00 PM",
                    "datetime": before_date,
                    "is_before_arrival": True
                })
            
            # Slot 2 & 3: After part arrival
            after_date_1 = part_arrival_date + timedelta(days=1)
            after_date_2 = part_arrival_date + timedelta(days=3)
            
            slots_to_show.append({
                "date": after_date_1.strftime("%B %d, %Y"),
                "day": after_date_1.strftime("%A"),
                "time": "10:00 AM - 12:00 PM",
                "datetime": after_date_1,
                "is_before_arrival": False
            })
            
            slots_to_show.append({
                "date": after_date_2.strftime("%B %d, %Y"),
                "day": after_date_2.strftime("%A"),
                "time": "2:00 PM - 4:00 PM",
                "datetime": after_date_2,
                "is_before_arrival": False
            })
        
        if len(slots_to_show) < 3:
            st.warning(f"Insufficient time slots available. Please contact support.")
            return None
        
        # Display slots with warnings
        st.markdown("### Select Time Slot")
        
        # Check if a slot was already selected
        if "combined_selected_slot_idx" in st.session_state:
            selected_slot = slots_to_show[st.session_state.combined_selected_slot_idx]
        else:
            selected_slot = None
        
        # Display all slots
        for idx, slot in enumerate(slots_to_show):
            is_selected = (selected_slot is not None and idx == st.session_state.get("combined_selected_slot_idx"))
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                slot_display = f"{slot['date']} - {slot['time']}"
                
                if slot['is_before_arrival']:
                    # Show warning for slot before part arrival
                    if is_selected:
                        st.markdown(f"**✓ {slot_display}** (Selected)")
                    else:
                        st.markdown(f"**{slot_display}**")
                    st.warning(f"⚠️ **Important Notice:** This time slot is scheduled **before** your part arrives on **{part_arrival_str}**. We strongly recommend selecting a time slot **after** the part arrival date to ensure the technician has the necessary part available for installation. Booking before part arrival may result in a rescheduled visit if the part has not been delivered.")
                else:
                    if is_selected:
                        st.markdown(f"**✓ {slot_display}** (Selected)")
                    else:
                        st.markdown(f"**{slot_display}**")
                    st.info(f"✓ This time slot is **after** part arrival on {part_arrival_str}")
            
            with col2:
                button_label = "✓ Selected" if is_selected else "Select"
                button_disabled = is_selected
                if st.button(button_label, key=f"slot_select_{idx}", use_container_width=True, disabled=button_disabled):
                    st.session_state.combined_selected_slot_idx = idx
                    selected_slot = slot
                    st.rerun()
        
        # Return selected slot if one is chosen
        if selected_slot:
            return selected_slot
        
        return None
    
    def _generate_tracking_id(self) -> str:
        """Generate a unique tracking ID for the order"""
        import random
        import string
        # Format: TRK-XXXXXX (6 alphanumeric characters)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TRK-{random_part}"
    
    def _generate_dispatch_tracking_id(self) -> str:
        """Generate a unique dispatch tracking ID for technician booking"""
        import random
        import string
        # Format: DSP-XXXXXX (6 alphanumeric characters)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"DSP-{random_part}"


def main():
    """Main entry point"""
    app = ApplianceTroubleshootApp()
    app.run()


# Streamlit requires code to run at module level
main()

