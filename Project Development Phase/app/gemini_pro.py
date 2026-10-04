import google.generativeai as genai
import os
import warnings
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=FutureWarning)

def generate_story(outline: list) -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("API Key missing!")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    formatted_outline = "\n".join([f"Panel {i+1}: {item.get('scene_description', '')}" for i, item in enumerate(outline)])
    
    prompt = f"""
    You are a comic book writer. Write a cohesive story with narration and dialogue for EXACTLY 2 panels based on this outline:
    {formatted_outline}
    
    CRITICAL RULE: You MUST separate the text for each panel using EXACTLY this delimiter: |||
    Example format:
    Narrator: ... Free says: ...
    |||
    Narrator: ...
    
    (Do not include 'Panel 1:' or any markdown. ONLY use ||| to separate the 2 panels).
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error generating story: {str(e)}")