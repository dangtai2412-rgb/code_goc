import google.generativeai as genai
import os
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

print("Danh sách model bạn có thể dùng:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")