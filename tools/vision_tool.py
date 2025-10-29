# tools/vision_tool.py (FINAL FIXED VERSION)
import os
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from crewai.tools.base_tool import BaseTool


class GeminiVisionTool(BaseTool):
    # Annotate fields so Pydantic v2 recognizes these as field overrides
    name: str = "gemini_vision_brand_analyzer"
    description: str = (
        "Analyzes a hero image URL and returns a detailed text description of "
        "its visual branding elements such as colors, design style, and emotional tone."
    )

    def _run(self, image_url: str) -> str:
        """
        Runs Gemini Pro Vision to analyze the given image URL.
        Returns a professional, detailed visual branding description.
        """
        if not image_url:
            return "⚠️ No image URL provided."

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "❌ Missing GOOGLE_API_KEY environment variable."

        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro-vision")

            # Fetch image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            # Open and analyze
            img = Image.open(BytesIO(response.content))
            prompt = (
                "You are a professional brand strategist. Analyze this image and describe:\n"
                "1. Primary colors (with hex codes)\n"
                "2. Secondary colors\n"
                "3. Design style (modern, minimal, luxurious, etc.)\n"
                "4. Emotional tone (trust, innovation, calm, etc.)\n"
                "5. Any logo or icon elements\n"
                "Provide a concise yet elegant branding summary."
            )

            result = model.generate_content([prompt, img])
            return result.text.strip()

        except Exception as e:
            return f"❌ Error analyzing image: {str(e)}"

    async def _arun(self, image_url: str) -> str:
        """
        Async version of the tool.
        """
        return self._run(image_url)
