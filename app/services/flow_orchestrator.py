"""Flow orchestrator using LangChain for managing conversation flows"""
from typing import Dict, List, Optional
from app.agents.appliance_type_agent import ApplianceTypeAgent
from app.agents.issue_listing_agent import IssueListingAgent
from app.agents.troubleshooting_agent import TroubleshootingAgent
from app.agents.summarization_agent import SummarizationAgent
from app.models.appliance import Appliance


class FlowOrchestrator:
    """Orchestrates the conversation flow using LangChain agents"""
    
    # Flow states
    FLOW_IDENTIFICATION = "identification"
    FLOW_ISSUE_LISTING = "issue_listing"
    FLOW_TROUBLESHOOTING = "troubleshooting"
    FLOW_BOOKING = "booking"
    
    def __init__(self):
        """Initialize flow orchestrator with agents"""
        try:
            self.appliance_type_agent = ApplianceTypeAgent()
            self.issue_listing_agent = IssueListingAgent()
            self.troubleshooting_agent = TroubleshootingAgent()
            self.summarization_agent = SummarizationAgent()
        except ValueError as e:
            print(f"Warning: {e}")
            self.appliance_type_agent = None
            self.issue_listing_agent = None
            self.troubleshooting_agent = None
            self.summarization_agent = None
    
    def detect_appliance_type(self, appliance: Appliance) -> Optional[str]:
        """Detect appliance type from details"""
        if not self.appliance_type_agent:
            return None
        
        try:
            appliance_type = self.appliance_type_agent.detect_type(
                brand=appliance.brand,
                model=appliance.model,
                serial=appliance.serial
            )
            return appliance_type
        except Exception as e:
            print(f"Error detecting appliance type: {e}")
            return None
    
    def list_common_issues(self, appliance: Appliance) -> List[str]:
        """List common issues for appliance type"""
        if not self.issue_listing_agent or not appliance.appliance_type:
            return []
        
        try:
            issues = self.issue_listing_agent.list_common_issues(
                appliance_type=appliance.appliance_type,
                brand=appliance.brand,
                model=appliance.model
            )
            return issues
        except Exception as e:
            print(f"Error listing issues: {e}")
            return []
    
    def get_troubleshooting_guidance(
        self,
        appliance: Appliance,
        issue: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """Get troubleshooting guidance"""
        if not self.troubleshooting_agent or not appliance.appliance_type:
            return "I'm unable to provide troubleshooting guidance at the moment."
        
        try:
            guidance = self.troubleshooting_agent.get_guidance(
                appliance_type=appliance.appliance_type,
                brand=appliance.brand,
                model=appliance.model,
                issue=issue,
                conversation_history=conversation_history
            )
            return guidance
        except Exception as e:
            print(f"Error getting troubleshooting guidance: {e}")
            return "I apologize, but I encountered an error. Please try again or book a technician."
    
    def summarize_issue(
        self,
        appliance: Appliance,
        conversation_history: List[Dict]
    ) -> str:
        """Summarize issue for booking"""
        if not self.summarization_agent or not appliance.appliance_type:
            return "Issue description not available."
        
        try:
            summary = self.summarization_agent.summarize_issue(
                appliance_type=appliance.appliance_type,
                brand=appliance.brand,
                model=appliance.model,
                conversation_history=conversation_history
            )
            return summary
        except Exception as e:
            print(f"Error summarizing issue: {e}")
            return "Issue description not available."
    
    def reset_troubleshooting_memory(self):
        """Reset troubleshooting agent memory"""
        if self.troubleshooting_agent:
            self.troubleshooting_agent.reset_memory()

