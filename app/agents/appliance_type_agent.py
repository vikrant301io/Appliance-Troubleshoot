"""LangChain agent for detecting appliance type"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.prompts.appliance_prompts import APPLIANCE_TYPE_DETECTION_PROMPT
import os


class ApplianceTypeAgent:
    """Agent for detecting appliance type from details"""
    
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
        self.prompt_template = ChatPromptTemplate.from_template(APPLIANCE_TYPE_DETECTION_PROMPT)
    
    def detect_type(self, brand: str, model: str, serial: str = None) -> str:
        """
        Detect appliance type from details
        
        Args:
            brand: Appliance brand
            model: Model number
            serial: Serial number (optional)
            
        Returns:
            Appliance type (e.g., "Refrigerator", "TV")
        """
        try:
            chain = self.prompt_template | self.llm
            response = chain.invoke({
                "brand": brand or "Unknown",
                "model": model or "Unknown",
                "serial": serial or "Unknown"
            })
            
            appliance_type = response.content.strip()
            
            # Clean up response (remove quotes, extra text)
            appliance_type = appliance_type.replace('"', '').replace("'", "").strip()
            
            # Validate common types
            common_types = [
                "Refrigerator", "Freezer", "Washing Machine", "Dishwasher",
                "TV", "Microwave", "Oven", "Stove", "Air Conditioner", "Dryer"
            ]
            
            for t in common_types:
                if t.lower() in appliance_type.lower():
                    return t
            
            return appliance_type if appliance_type else "Unknown"
        except Exception as e:
            print(f"Error detecting appliance type: {e}")
            return "Unknown"

