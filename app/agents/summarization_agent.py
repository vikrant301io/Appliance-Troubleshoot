"""LangChain agent for summarizing issues"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.prompts.troubleshooting_prompts import ISSUE_SUMMARIZATION_PROMPT
import os
from typing import List, Dict


class SummarizationAgent:
    """Agent for summarizing issues for technician booking"""
    
    def __init__(self, api_key: str = None):
        """Initialize the agent"""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=api_key
        )
        self.prompt_template = ChatPromptTemplate.from_template(ISSUE_SUMMARIZATION_PROMPT)
    
    def summarize_issue(
        self,
        appliance_type: str,
        brand: str,
        model: str,
        conversation_history: List[Dict]
    ) -> str:
        """
        Summarize the issue for technician booking
        
        Args:
            appliance_type: Type of appliance
            brand: Brand name
            model: Model number
            conversation_history: Conversation messages
            
        Returns:
            Issue summary text
        """
        try:
            # Format conversation history
            history_text = ""
            if conversation_history:
                for msg in conversation_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    history_text += f"{role.capitalize()}: {content}\n"
            
            chain = self.prompt_template | self.llm
            response = chain.invoke({
                "appliance_type": appliance_type,
                "brand": brand,
                "model": model,
                "conversation_history": history_text or "No conversation history."
            })
            
            return response.content.strip()
        except Exception as e:
            print(f"Error summarizing issue: {e}")
            return "Issue description not available."

