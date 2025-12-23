"""AI client for interacting with AI services."""

import logging
from typing import Optional, List
import os

from src.core.config import Config


class AIClient:
    """Unified AI client for various AI services."""
    
    def __init__(self, config: Config):
        """Initialize AI client."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.AIClient")
        
        # Initialize clients based on available API keys
        self.openai_client = None
        self.anthropic_client = None
        
        if config.openai_api_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=config.openai_api_key)
                self.logger.info("OpenAI client initialized")
            except ImportError:
                self.logger.warning("OpenAI library not installed")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI: {e}")
        
        if config.anthropic_api_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=config.anthropic_api_key)
                self.logger.info("Anthropic client initialized")
            except ImportError:
                self.logger.warning("Anthropic library not installed")
            except Exception as e:
                self.logger.error(f"Failed to initialize Anthropic: {e}")
    
    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using available AI service.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        # Try OpenAI first
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.config.default_llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                self.logger.error(f"OpenAI generation failed: {e}")
        
        # Try Anthropic
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                self.logger.error(f"Anthropic generation failed: {e}")
        
        # Fallback: return template response
        self.logger.warning("No AI service available, using template response")
        return self._generate_template_response(prompt)
    
    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> Optional[str]:
        """
        Generate an image using AI.
        
        Args:
            prompt: Image description
            size: Image size
            quality: Image quality
            
        Returns:
            Path to generated image or None
        """
        if self.openai_client:
            try:
                response = self.openai_client.images.generate(
                    model=self.config.default_image_model,
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=1
                )
                return response.data[0].url
            except Exception as e:
                self.logger.error(f"Image generation failed: {e}")
        
        return None
    
    def _generate_template_response(self, prompt: str) -> str:
        """Generate a template response when no AI is available."""
        if "character" in prompt.lower():
            return '''[
                {
                    "name": "Alex Stone",
                    "description": "A determined protagonist facing incredible odds.",
                    "role": "protagonist",
                    "personality_traits": ["brave", "intelligent", "resourceful"],
                    "emotional_arc": "Transforms from skeptical outsider to confident hero"
                },
                {
                    "name": "Sam Rivera",
                    "description": "Loyal companion with a mysterious past.",
                    "role": "supporting",
                    "personality_traits": ["loyal", "witty", "protective"],
                    "emotional_arc": "Learns to trust and open up to others"
                }
            ]'''
        elif "scene" in prompt.lower():
            return '''[
                {
                    "scene_type": "EXT.",
                    "location": "CITY STREET",
                    "time": "DAY",
                    "action": "Our hero walks through the bustling city, unaware of the adventure that awaits.",
                    "dialogue": [
                        {"character": "Alex", "line": "Just another ordinary day..."},
                        {"character": "Sam", "line": "You say that every time before something crazy happens."}
                    ]
                },
                {
                    "scene_type": "INT.",
                    "location": "OFFICE",
                    "time": "DAY",
                    "action": "The discovery of a mysterious message changes everything.",
                    "dialogue": [
                        {"character": "Alex", "line": "This can't be real."},
                        {"character": "Sam", "line": "But it is. And we need to act fast."}
                    ]
                }
            ]'''
        elif "logline" in prompt.lower():
            return "An ordinary person discovers an extraordinary secret that will change their life forever."
        else:
            return "This is a template response generated without AI services."
