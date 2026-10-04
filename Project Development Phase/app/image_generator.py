import os
import re
import urllib.request
from urllib.parse import quote
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import ssl
import random
import time
from dotenv import load_dotenv

load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context

proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

def sanitize_filename(prompt):
    clean = re.sub(r'[^a-zA-Z0-9]', '_', str(prompt))[:30]
    return f"panel_{clean}_{random.randint(1000, 9999)}.jpg"

def generate_image(prompt, filename=None):
    if not prompt: prompt = "Comic scene"
    if not filename: filename = sanitize_filename(prompt)
        
    path = f"static/panels/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    safe_prompt = quote(str(prompt)[:120])
    hf_token = os.getenv("HF_API_KEY")

    print(f"\n🚀 Starting Image Generation for Panel...")

    try:
        print("📡 Trying Engine 1 (Pollinations AI)...")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?seed={random.randint(1,100000)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                img = Image.open(io.BytesIO(response.read())).convert('RGB')
                img.save(path, format='JPEG', quality=95)
                print("✅ Success via Engine 1 (Pollinations)!")
                time.sleep(2)
                return path
    except Exception as e:
        print(f"❌ Engine 1 Blocked ({e}). Switching instantly to Engine 2...")

    if hf_token:
        try:
            print("📡 Trying Engine 2 (Hugging Face Diffusers)...")
            hf_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            }
            payload = {"inputs": f"{prompt}, high quality comic book art style, vibrant colors"}
            data = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(hf_url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=35) as response:
                if response.status == 200:
                    img = Image.open(io.BytesIO(response.read())).convert('RGB')
                    img.save(path, format='JPEG', quality=95)
                    print("✅ Success via Engine 2 (Hugging Face)!")
                    return path
        except Exception as e:
            print(f"❌ Engine 2 Error: {e}")
    else:
        print("⚠️ Engine 2 Skipped: HF_API_KEY missing in .env file!")

    print("⚠️ All routes exhausted. Using Fallback text image.")
    img = Image.new('RGB', (512, 512), color=(40, 40, 50))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    lines = textwrap.wrap(prompt, width=45)
    y = 200
    for line in lines:
        draw.text((40, y), line, fill=(255, 220, 100), font=font)
        y += 20
    img.save(path, format='JPEG')
    return path