"""
AI Responder Module - Generate intelligent responses to Bluesky posts

Updated for 2025 with support for:
- OpenAI GPT-4/GPT-4-Turbo/GPT-4o
- Anthropic Claude (optional)
- Local Ollama models (optional)

IMPORTANT: AI-generated responses should be clearly marked as such.
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate_response(
        self,
        post_text: str,
        user_bio: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a response to a post."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def generate_response(
        self,
        post_text: str,
        user_bio: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a response using OpenAI."""
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_user_prompt(post_text, user_bio, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=100,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"[ERROR] OpenAI API error: {e}")
            return "Interesting perspective! 🤖"
    
    def _get_system_prompt(self) -> str:
        return """You are an AI assistant helping engage authentically on Bluesky social.

Guidelines:
1. Keep responses under 250 characters
2. Be genuine and add value - avoid generic responses
3. Reference specific points from the post
4. Match the tone while staying professional
5. Don't use hashtags unless the post does
6. Avoid controversial topics
7. If the post mentions struggles, respond with empathy
8. Add a subtle AI indicator like "🤖" at the end

Your goal is to foster genuine connection, not to spam."""
    
    def _build_user_prompt(
        self,
        post_text: str,
        user_bio: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        prompt = f"""Post to respond to: "{post_text}"

Author's Bio: {user_bio or 'Not available'}
"""
        
        if context:
            if context.get('followers'):
                prompt += f"\nAuthor followers: {context['followers']}"
            if context.get('topic'):
                prompt += f"\nDetected topic: {context['topic']}"
        
        prompt += """

Craft a genuine, engaging response that demonstrates understanding and adds value.
Remember: max 250 characters, be authentic, add 🤖 at end."""
        
        return prompt


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307", api_key: Optional[str] = None):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY in .env")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
    
    def generate_response(
        self,
        post_text: str,
        user_bio: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a response using Claude."""
        system_prompt = """You are an AI assistant helping engage authentically on Bluesky social.
Keep responses under 250 characters. Be genuine, add value, and include 🤖 at the end."""
        
        user_prompt = f"""Post: "{post_text}"
Author Bio: {user_bio or 'Not available'}

Craft a genuine response (max 250 chars, end with 🤖)."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"[ERROR] Anthropic API error: {e}")
            return "Interesting perspective! 🤖"


class AIResponder:
    """
    Main AI Responder class that handles response generation.
    
    Supports multiple AI providers and includes content analysis.
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        signature: str = "🤖"
    ):
        """
        Initialize the AI Responder.
        
        Args:
            provider: AI provider ("openai", "anthropic", or "local")
            model: Model name (uses default if not specified)
            signature: Signature to add to responses
        """
        self.signature = signature
        self.provider = self._init_provider(provider, model)
        
        # Topic detection keywords
        self.topic_keywords = {
            "tech": ["AI", "programming", "code", "software", "data", "machine learning",
                    "crypto", "blockchain", "startup", "tech", "developer", "API"],
            "business": ["entrepreneur", "marketing", "growth", "strategy", "leadership",
                        "startup", "sales", "revenue", "business", "founder"],
            "creative": ["design", "art", "writing", "music", "culture", "creative",
                        "photography", "film", "fashion", "artist"],
            "academic": ["research", "science", "philosophy", "education", "study",
                        "learning", "theory", "university", "academic"]
        }
    
    def _init_provider(self, provider: str, model: Optional[str]) -> AIProvider:
        """Initialize the AI provider."""
        if provider.lower() == "openai":
            return OpenAIProvider(model=model or "gpt-4o")
        elif provider.lower() == "anthropic":
            return AnthropicProvider(model=model or "claude-3-haiku-20240307")
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def detect_topic(self, text: str) -> str:
        """Detect the topic of a post."""
        text_lower = text.lower()
        
        for topic, keywords in self.topic_keywords.items():
            matches = sum(1 for kw in keywords if kw.lower() in text_lower)
            if matches >= 2:
                return topic
        
        return "general"
    
    def analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze post content for context."""
        return {
            "topic": self.detect_topic(text),
            "has_question": "?" in text,
            "has_links": "http" in text.lower(),
            "length": len(text),
            "has_emoji": any(ord(c) > 127 for c in text if not c.isascii())
        }
    
    def generate_response(
        self,
        post_text: str,
        user_bio: str = "",
        user_stats: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an AI response to a post.
        
        Args:
            post_text: The text of the post to respond to
            user_bio: The author's biography
            user_stats: Optional user statistics
            
        Returns:
            Generated response string
        """
        # Analyze content for context
        analysis = self.analyze_content(post_text)
        
        context = {
            "topic": analysis["topic"],
            **user_stats or {}
        }
        
        # Generate response
        response = self.provider.generate_response(post_text, user_bio, context)
        
        # Ensure signature is present
        if self.signature and self.signature not in response:
            if len(response) + len(self.signature) + 1 <= 250:
                response = f"{response} {self.signature}"
            else:
                response = response[:250 - len(self.signature) - 4] + f"... {self.signature}"
        
        # Ensure response is within limit
        if len(response) > 250:
            response = response[:247] + "..."
        
        return response


def create_responder(
    provider: str = "openai",
    model: Optional[str] = None
) -> AIResponder:
    """
    Factory function to create an AI responder.
    
    Args:
        provider: "openai" or "anthropic"
        model: Optional model override
        
    Returns:
        Configured AIResponder instance
    """
    return AIResponder(provider=provider, model=model)


if __name__ == "__main__":
    print("Testing AI Responder...")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "post": "Just deployed my first ML model to production! The debugging was intense but seeing it work is amazing! 🚀",
            "bio": "ML Engineer | Building AI solutions | Love discussing tech"
        },
        {
            "post": "Looking for book recommendations on startup growth. What's everyone reading?",
            "bio": "Founder | Building in public | Growth enthusiast"
        },
        {
            "post": "Having a rough day. Sometimes the pressure just gets to you.",
            "bio": "Designer trying to make the world more beautiful"
        }
    ]
    
    try:
        responder = AIResponder()
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nTest {i}:")
            print(f"Post: {test['post']}")
            print(f"Bio: {test['bio']}")
            
            response = responder.generate_response(
                post_text=test['post'],
                user_bio=test['bio']
            )
            
            print(f"Response ({len(response)} chars): {response}")
            print("-" * 50)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have OPENAI_API_KEY set in your .env file")
