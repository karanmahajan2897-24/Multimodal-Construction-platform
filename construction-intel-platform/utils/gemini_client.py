"""
Gemini API client wrapper with graceful fallback to demo mode.
"""

import json
import base64
import re
import google.generativeai as genai
from PIL import Image
import io


def init_gemini(api_key: str):
    """Initialize Gemini client with provided API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def call_gemini_vision(model, prompt: str, image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    """Call Gemini Vision API with an image and prompt."""
    img = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([prompt, img])
    return response.text


def call_gemini_text(model, prompt: str) -> str:
    """Call Gemini text API with a prompt."""
    response = model.generate_content(prompt)
    return response.text


def extract_json_from_response(text: str) -> dict:
    """Safely extract JSON from Gemini's response text."""
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block from markdown code fences
    pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(pattern, text)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    # Try finding first { ... } block
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    return {}
