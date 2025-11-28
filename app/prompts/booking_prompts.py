"""Prompt templates for booking flow"""

ISSUE_LISTING_PROMPT = """You are helping a customer identify common issues with their appliance.

Appliance Type: {appliance_type}
Brand: {brand}
Model: {model}

Based on this appliance type, provide a list of 5-10 most common issues that customers typically face with this type of appliance.

Format as a numbered list:
1. [Issue description]
2. [Issue description]
...

Be specific and use common language that customers would use to describe problems."""

