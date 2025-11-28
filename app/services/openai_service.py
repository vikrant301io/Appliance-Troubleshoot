import json
import base64
import os
from typing import Tuple, Dict, Optional
from openai import OpenAI


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_appliance_info(self, text: str) -> Dict:
        """Extract appliance information from text using GPT"""
        prompt = """Extract appliance information from the following text. Return a JSON object with:
- brand: the appliance brand (e.g., Samsung, LG, Whirlpool)
- model: the model number
- serial: the serial number
- age: estimated age in years (if mentioned, otherwise null)

Text: {text}

Return ONLY valid JSON, no other text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts structured information from text. Always return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt.format(text=text)
                    }
                ],
                temperature=0.3
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            raise Exception(f"Error extracting appliance info: {e}")
    
    def read_nameplate_image(self, image_bytes: bytes) -> Tuple[str, Dict]:
        """Read text from nameplate image using OpenAI Vision API"""
        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Read all text from this appliance nameplate image. Extract:
1. Brand name
2. Model number
3. Serial number
4. Any date or age information

Return the raw text you see, and then provide a JSON object with:
{
  "brand": "brand name or null",
  "model": "model number or null",
  "serial": "serial number or null",
  "age": estimated age in years or null
}

Format your response as:
RAW_TEXT: [all text you see]
JSON: [the JSON object]"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            # Parse the response
            text_content = ""
            info = {}
            
            if "RAW_TEXT:" in result_text and "JSON:" in result_text:
                parts = result_text.split("JSON:")
                text_content = parts[0].replace("RAW_TEXT:", "").strip()
                json_part = parts[1].strip()
                try:
                    info = json.loads(json_part)
                except json.JSONDecodeError:
                    pass
            else:
                text_content = result_text
                # Try to extract JSON if present
                try:
                    if "{" in result_text and "}" in result_text:
                        json_start = result_text.find("{")
                        json_end = result_text.rfind("}") + 1
                        info = json.loads(result_text[json_start:json_end])
                except json.JSONDecodeError:
                    pass
            
            return text_content, info
        except Exception as e:
            raise Exception(f"Error reading image: {e}")
    
    def get_nameplate_guidance(self, category: str, subcategory: str, brand: str) -> str:
        """Get nameplate location guidance using GPT-4 with YouTube video links"""
        prompt = f"""You are a friendly and practical appliance expert who explains things clearly, naturally, and without sounding like an AI or using robotic/LLM-like language.

When a user asks where to find the model number, serial number, or nameplate for an appliance, your job is:

1. Give a short, simple explanation in plain language.

2. Provide a clear step-by-step guide.

3. Keep the tone conversational, like a technician helping someone in person.

4. Avoid robotic phrasing like "as an AI," "based on my dataset," "here is the guide you requested," or suggesting users search for images online.

Always tailor the explanation to:

- Appliance Category: {category}

- Subcategory: {subcategory}

- Brand: {brand}

If the appliance is a GE compact or mini fridge, explain the typical location inside the fridge compartment and describe what the nameplate/tag normally looks like.

Your goal is to make the user feel they're getting real help from an expert technician.

Please provide guidance on where to find the model number, serial number, and nameplate for a {brand} {subcategory}. Include specific locations, what the nameplate typically looks like, and any tips for finding it easily.

IMPORTANT: At the end of your response, provide 2-3 helpful YouTube video links (actual working YouTube URLs) that show how to find the nameplate/model number/serial number for a {brand} {subcategory}. Format the links as clickable markdown links like this:

**Helpful Video Tutorials:**
- [Video Title 1](https://www.youtube.com/watch?v=...)
- [Video Title 2](https://www.youtube.com/watch?v=...)
- [Video Title 3](https://www.youtube.com/watch?v=...)

Make sure the video links are real, working YouTube URLs that are relevant to finding nameplates for this specific brand and subcategory."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly and practical appliance expert. Provide clear, conversational guidance with helpful descriptions of what nameplates look like and where to find them. Always include 2-3 relevant YouTube video links at the end of your response for the specific brand and subcategory."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting nameplate guidance: {e}")

