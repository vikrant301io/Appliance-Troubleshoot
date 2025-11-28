"""Prompt templates for LangChain agents"""
from .appliance_prompts import (
    APPLIANCE_TYPE_DETECTION_PROMPT,
    APPLIANCE_CONFIRMATION_PROMPT
)
from .troubleshooting_prompts import (
    TROUBLESHOOTING_GUIDE_PROMPT,
    ISSUE_SUMMARIZATION_PROMPT
)
from .booking_prompts import (
    ISSUE_LISTING_PROMPT
)

__all__ = [
    "APPLIANCE_TYPE_DETECTION_PROMPT",
    "APPLIANCE_CONFIRMATION_PROMPT",
    "TROUBLESHOOTING_GUIDE_PROMPT",
    "ISSUE_SUMMARIZATION_PROMPT",
    "ISSUE_LISTING_PROMPT"
]

