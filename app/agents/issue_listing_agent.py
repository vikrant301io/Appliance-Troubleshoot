"""LangChain agent for listing common issues"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.prompts.booking_prompts import ISSUE_LISTING_PROMPT
import os
from typing import List


class IssueListingAgent:
    """Agent for listing common issues for an appliance type"""
    
    def __init__(self, api_key: str = None):
        """Initialize the agent"""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=api_key
        )
        self.prompt_template = ChatPromptTemplate.from_template(ISSUE_LISTING_PROMPT)
    
    def list_common_issues(self, appliance_type: str, brand: str = None, model: str = None) -> List[str]:
        """
        List common issues for an appliance type
        
        Args:
            appliance_type: Type of appliance
            brand: Brand name (optional)
            model: Model number (optional)
            
        Returns:
            List of common issues
        """
        try:
            chain = self.prompt_template | self.llm
            response = chain.invoke({
                "appliance_type": appliance_type,
                "brand": brand or "Unknown",
                "model": model or "Unknown"
            })
            
            # Parse numbered list from response
            issues = []
            lines = response.content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Remove numbering (1., 2., etc.)
                import re
                line = re.sub(r'^\d+[\.\)]\s*', '', line)
                line = line.strip()
                
                if line and len(line) > 5:  # Filter out very short lines
                    issues.append(line)
            
            # Return 5-10 issues
            return issues[:10] if issues else []
        except Exception as e:
            print(f"Error listing issues: {e}")
            return []

