import json
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.8-flash"

def analyze_construction_image(image_bytes: bytes, mime_type: str, api_key: str, analysis_type: str) -> dict:
    """Send an image to Gemini and parse the JSON response."""
    if analysis_type == "safety":
        prompt = """
Analyze this construction-site image for visible PPE and potential hazards.
Assess helmets, high-visibility vests, boots, and harnesses only where visible.
Do not assume an item is absent if it cannot be seen. Return JSON with:
safety_score (0-100 or null), overall_status, ppe_detection (object),
hazards (list of objects with hazard, severity, evidence, remedy),
limitations. This is not a formal regulatory inspection.
"""
    elif analysis_type == "cracks":
        prompt = """
Review this concrete or wall image for visible defects. Return JSON with:
defect_type, estimated_width_mm (number or null), possible_causes (list),
recommended_inspection, urgency, limitations. Possible categories include
hairline, settlement, structural shear, thermal expansion, and spalling.
Do not invent a precise width when no scale is visible. Do not certify structural safety.
"""
    else:
        raise ValueError("analysis_type must be 'safety' or 'cracks'")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt + "\nReturn only valid JSON."
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    if not response.text:
        raise ValueError("The AI returned an empty response.")
    return json.loads(response.text)
