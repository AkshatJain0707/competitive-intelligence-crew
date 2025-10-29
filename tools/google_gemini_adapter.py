"""Minimal adapter to call Google Generative AI (Gemini) via google.generativeai.

This provides a simple `call` method compatible with code that expects an LLM-like
object. It does not implement streaming. Keep this minimal and explicit.
"""
import os
from typing import Any
try:
    import google.generativeai as genai
except Exception:
    genai = None

from crewai.llms.base_llm import BaseLLM


class GoogleGeminiAdapter(BaseLLM):
    """CrewAI-compatible adapter that calls Google Generative AI (Gemini).

    This subclasses CrewAI's BaseLLM so the runtime treats it as a native
    LLM implementation and does not attempt to create a litellm/OpenAI client
    from a model string.
    """

    def __init__(self, api_key: str, model: str = "gemini-pro") -> None:
        if genai is None:
            raise RuntimeError("google.generativeai library not installed")
        super().__init__(model=model, api_key=api_key, provider="google")
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=api_key)
        self._client = genai.GenerativeModel(model)

    def call(self, messages: str | list[dict] | None, tools: list[dict] | None = None, callbacks: list[Any] | None = None, available_functions: dict[str, Any] | None = None, from_task: Any | None = None, from_agent: Any | None = None) -> str | Any:
        """Call Gemini and return the generated text.

        Accepts either a string prompt or a list of message dicts (role/content).
        """
        if isinstance(messages, list):
            prompt = "\n".join(m.get("content", "") for m in messages)
        else:
            prompt = str(messages or "")

        if not prompt.strip():
            return "No content provided"

        try:
            response = self._client.generate_content(prompt)
            if response.text:
                return response.text
            return "No response text generated"
        except Exception as e:
            error_msg = str(e)
            if "SERVICE_DISABLED" in error_msg or "not been used" in error_msg:
                print(f"\n⚠️  Generative Language API not enabled in GCP project.")
                print(f"Enable it at: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
                raise RuntimeError("Generative Language API is not enabled. Please enable it in Google Cloud Console.")
            print(f"Gemini API error: {e}")
            raise
