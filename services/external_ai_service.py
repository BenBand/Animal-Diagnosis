"""
External AI Service Module
Handles integration with OpenAI and other LLM providers for dynamic responses
"""
import os
import json
import requests
from typing import Optional, Dict, Any
from config import OPENAI_API_KEY, HUGGINGFACE_TOKEN

# Try to import openai - will work if installed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ExternalAIService:
    """
    Service to fetch real-time responses from external AI providers
    Supports OpenAI GPT and HuggingFace Inference API
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.openai_api_key = OPENAI_API_KEY
        self.huggingface_token = HUGGINGFACE_TOKEN
        self.provider = 'openai' if OPENAI_API_KEY else ('huggingface' if HUGGINGFACE_TOKEN else 'fallback')
        
        if OPENAI_AVAILABLE and self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def is_available(self) -> bool:
        """Check if external AI service is configured"""
        return bool(self.openai_api_key) or bool(self.huggingface_token)
    
    def get_response(self, user_query: str, context: str = "") -> Optional[str]:
        """
        Get response from external AI for agricultural questions
        
        Args:
            user_query: The user's question
            context: Additional context about livestock/agriculture topic
            
        Returns:
            AI-generated response or None if unavailable
        """
        if not self.is_available():
            return None
        
        # Build agricultural system prompt
        system_prompt = self._build_agricultural_prompt(context)
        
        if self.provider == 'openai' and self.openai_api_key:
            return self._get_openai_response(user_query, system_prompt)
        elif self.huggingface_token:
            return self._get_huggingface_response(user_query, system_prompt)
        
        return None
    
    def _build_agricultural_prompt(self, context: str) -> str:
        """Build system prompt for agricultural assistant"""
        base_prompt = """You are an expert livestock and agricultural assistant helping farmers. 
Provide accurate, practical, and actionable advice about:
- Cattle, poultry, goats, sheep farming
- Animal nutrition and feed management
- Disease prevention and treatment
- Breeding and herd management
- Pasture and grazing management
- Farm equipment and infrastructure
- Market prices and financial planning

Always prioritize animal welfare and sustainable farming practices.
If you don't know something, say so honestly."""
        
        if context:
            base_prompt += f"\n\nContext: {context}"
        
        return base_prompt
    
    def _get_openai_response(self, user_query: str, system_prompt: str) -> Optional[str]:
        """Get response from OpenAI API"""
        if not OPENAI_AVAILABLE:
            return None
            
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return None
    
    def _get_huggingface_response(self, user_query: str, system_prompt: str) -> Optional[str]:
        """Get response from HuggingFace Inference API (free tier)"""
        try:
            # Using a free conversational model
            API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            payload = {
                "inputs": f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_query} [/INST]",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()[0]['generated_text']
            return None
        except Exception as e:
            print(f"HuggingFace API Error: {e}")
            return None


class FallbackResponseGenerator:
    """
    Generates intelligent fallback responses when AI is unavailable
    Uses curated agricultural knowledge
    """
    
    def __init__(self):
        self.topic_keywords = {
            'disease': ['disease', 'sick', 'illness', 'symptom', 'fever', 'cough', 'treatment'],
            'nutrition': ['feed', 'food', 'eat', 'nutrition', 'protein', 'vitamin', 'grass', 'hay'],
            'breeding': ['breed', 'baby', 'calf', 'pregnant', 'birth', 'mating', 'reproduce'],
            'housing': ['shelter', 'barn', 'fence', 'pen', 'housing', 'temperature', 'ventilation'],
            'market': ['price', 'cost', 'sell', 'buy', 'market', 'profit', 'money'],
            'weather': ['weather', 'rain', 'drought', 'heat', 'cold', 'climate'],
            'general': ['care', 'manage', 'farm', 'livestock', 'animal']
        }
    
    def generate(self, user_query: str) -> str:
        """Generate contextual fallback response based on query keywords"""
        query_lower = user_query.lower()
        
        # Detect topic from keywords
        detected_topics = []
        for topic, keywords in self.topic_keywords.items():
            if any(kw in query_lower for kw in keywords):
                detected_topics.append(topic)
        
        if not detected_topics:
            detected_topics = ['general']
        
        # Build response based on detected topics
        return self._build_topic_response(detected_topics, query_lower)
    
    def _build_topic_response(self, topics: list, query: str) -> str:
        """Build response for detected topics"""
        
        responses = {
            'disease': "For disease-related questions, I recommend: 1) Check for visible symptoms like coughing, lethargy, or loss of appetite. 2) Isolate sick animals immediately. 3) Consult a veterinarian promptly. 4) Maintain proper vaccination schedules. For specific concerns, I can search external veterinary databases for more information.",
            
            'nutrition': "For nutrition advice: Ensure clean water is always available. Feed quality varies by animal type and age. Common feeds include grasses, hay, grains, and commercial pellets. Consider consulting a nutritionist for balanced rations. Would you like specific feeding guidelines for a particular animal?",
            
            'breeding': "Breeding best practices: 1) Know the optimal breeding age for your species. 2) Maintain breeding records. 3) Provide proper nutrition during pregnancy. 4) Prepare for birth/calving with clean, dry facilities. 5) Have a veterinarian contact ready.",
            
            'housing': "Proper housing considerations: 1) Adequate space per animal. 2) Good ventilation to prevent respiratory issues. 3) Clean, dry bedding. 4) Protection from extreme weather. 5) Easy access to water and feeding areas. 6) Regular cleaning schedule.",
            
            'market': "For market information: Prices vary by region, season, and quality. Check local agricultural extension offices or market boards for current prices. Consider direct-to-consumer sales for better margins. Record all expenses for profit calculation.",
            
            'weather': "Weather impacts livestock: 1) Provide shade and water during heat. 2) Ensure shelter from rain and cold. 3) Monitor for heat stress in summer. 4) Adjust feed during extreme weather. 5) Have emergency plans for severe conditions.",
            
            'general': "I can provide information on various livestock topics. Please ask specific questions about cattle, poultry, goats, sheep, feeding, health, breeding, or farm management. For detailed advice, consulting local agricultural extension services is recommended."
        }
        
        # Combine relevant responses
        combined = []
        for topic in topics:
            if topic in responses:
                combined.append(responses[topic])
        
        return "\n\n".join(combined[:2])  # Limit to 2 topics to avoid too long response


# Singleton instances
_ai_service = None
_fallback_generator = None


def get_ai_service(config: Optional[Dict] = None) -> ExternalAIService:
    """Get or create ExternalAIService singleton"""
    global _ai_service
    if _ai_service is None:
        _ai_service = ExternalAIService(config)
    return _ai_service


def get_fallback_generator() -> FallbackResponseGenerator:
    """Get or create FallbackResponseGenerator singleton"""
    global _fallback_generator
    if _fallback_generator is None:
        _fallback_generator = FallbackResponseGenerator()
    return _fallback_generator


if __name__ == "__main__":
    # Test the service
    service = ExternalAIService()
    print(f"AI Service Available: {service.is_available()}")
    
    if service.is_available():
        response = service.get_response("What is the best feed for dairy cows?")
        print(f"AI Response: {response}")
    else:
        print("Configure OPENAI_API_KEY or HUGGINGFACE_TOKEN to enable AI responses")
        fallback = FallbackResponseGenerator()
        print(f"Fallback: {fallback.generate('my cow is sick')}")
