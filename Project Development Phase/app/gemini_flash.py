import google.generativeai as genai
import os
import json
import warnings
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=FutureWarning)

def generate_outline(user_prompt: str) -> list:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("API Key kaanom vro!")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash-lite')
    
    prompt = f"""
    You are a professional AI comic planner.
    Your task is to generate a strictly formatted JSON array containing EXACTLY 2 panel descriptions for a comic based on the story idea below:
    STORY: "{user_prompt}"
    
    Each JSON object must include:
    - "panel" (integer, 1 and 2)
    - "title" (string)
    - "scene_description" (string)
    - "image_prompt" (string)
    
    Respond ONLY in this valid JSON format, without any explanations or markdown.
    """
    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()
            
        panel_data = json.loads(output_text)
        return panel_data
    except Exception as e:
        raise Exception(f"Outline generation failed: {str(e)}")