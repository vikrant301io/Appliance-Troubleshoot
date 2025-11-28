"""Troubleshooting agent using direct OpenAI API"""
from openai import OpenAI
import os
import re
from typing import List, Dict
from app.prompts.troubleshooting_prompts import TROUBLESHOOTING_GUIDE_PROMPT
from app.utils.parts_loader import PartsLoader


class TroubleshootingAgent:
    """Agent for providing step-by-step troubleshooting guidance"""
    
    def __init__(self, api_key: str = None):
        """Initialize the agent"""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
    
    def get_guidance(
        self,
        appliance_type: str,
        brand: str,
        model: str,
        issue: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Get troubleshooting guidance using direct OpenAI API
        
        Args:
            appliance_type: Type of appliance
            brand: Brand name
            model: Model number
            issue: Issue description
            conversation_history: Previous conversation messages
            
        Returns:
            Troubleshooting guidance text
        """
        try:
            # Format conversation history
            history_text = ""
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    history_text += f"{role.capitalize()}: {content}\n"
            
            # Check if this is a special issue with parts (don't show part info from API)
            is_special_issue = PartsLoader.is_special_issue(issue)
            
            # Build the prompt - modify for special issues to exclude part information
            if is_special_issue:
                # Use a modified prompt that doesn't ask for part information
                prompt_template = """You are an expert appliance repair technician providing step-by-step troubleshooting guidance to a customer.

Appliance Details:
- Type: {appliance_type}
- Brand: {brand}
- Model: {model}
- Issue: {issue_description}

Conversation History:
{conversation_history}

Provide clear, numbered, step-by-step troubleshooting instructions. Be specific and safety-conscious.

Guidelines:
1. Start with the simplest solutions first
2. Include safety warnings when necessary
3. Be specific about what to check and how
4. After each step, ask if the issue is resolved
5. If troubleshooting becomes complex or unsafe, recommend booking a technician
6. DO NOT include any part information, part numbers, or costs in your response
7. DO NOT mention specific parts to order - just provide troubleshooting steps

Format your response as:
1. Step 1: [Description]
2. Step 2: [Description]
...

Continue the conversation naturally, asking if the user needs help with the next step."""
                
                prompt = prompt_template.format(
                    appliance_type=appliance_type or "Unknown",
                    brand=brand or "Unknown",
                    model=model or "Unknown",
                    issue_description=issue,
                    conversation_history=history_text or "No previous conversation."
                )
            else:
                prompt = TROUBLESHOOTING_GUIDE_PROMPT.format(
                    appliance_type=appliance_type or "Unknown",
                    brand=brand or "Unknown",
                    model=model or "Unknown",
                    issue_description=issue,
                    conversation_history=history_text or "No previous conversation."
                )
            
            # Call OpenAI API directly
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert appliance repair technician providing step-by-step troubleshooting guidance to customers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            guidance = response.choices[0].message.content.strip()
            
            # For special issues, filter out any part information that might have been included
            if is_special_issue:
                # Remove part information patterns
                guidance = re.sub(r'\*\*Part Required\*\*:.*?(?=\n\n|\n\*\*|$)', '', guidance, flags=re.IGNORECASE | re.DOTALL)
                guidance = re.sub(r'\*\*Part Number\*\*:.*?(?=\n\n|\n\*\*|$)', '', guidance, flags=re.IGNORECASE | re.DOTALL)
                guidance = re.sub(r'\*\*Cost\*\*:.*?(?=\n\n|\n\*\*|$)', '', guidance, flags=re.IGNORECASE | re.DOTALL)
                guidance = re.sub(r'If you want to order the part.*?(?=\n\n|$)', '', guidance, flags=re.IGNORECASE | re.DOTALL)
                guidance = re.sub(r'order.*?part.*?technician.*?bring.*?install.*?(?=\n\n|$)', '', guidance, flags=re.IGNORECASE | re.DOTALL)
                # Clean up any double newlines
                guidance = re.sub(r'\n\n\n+', '\n\n', guidance)
                guidance = guidance.strip()
            
            return guidance
            
        except Exception as e:
            print(f"Error getting troubleshooting guidance: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: try with a simpler direct call
            try:
                fallback_prompt = f"""You are an expert appliance repair technician. Provide step-by-step troubleshooting guidance.

Appliance Details:
- Type: {appliance_type or 'Unknown'}
- Brand: {brand or 'Unknown'}
- Model: {model or 'Unknown'}
- Issue: {issue}

Provide clear, numbered, step-by-step troubleshooting instructions. Start with the simplest solutions first. Include safety warnings when necessary."""
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": fallback_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content.strip()
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
                return f"I apologize, but I encountered an error while providing troubleshooting guidance. Please try again or consider booking a technician."
    
    def reset_memory(self):
        """Reset conversation memory (no-op for direct API approach)"""
        pass
