import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

# Configure both APIs
gemini_key = os.getenv('GEMINI_API_KEY')
groq_key = os.getenv('GROQ_API_KEY')

if gemini_key:
    genai.configure(api_key=gemini_key)

if groq_key:
    groq_client = Groq(api_key=groq_key)

def analyze_transcript(transcript, use_groq=True):
    """Analyze transcript and find viral moments"""
    
    prompt_text = f"""Analyze this video and create 3 viral clip moments (30-60 seconds each).

Video Info:
{transcript[:2000]}

Return ONLY this JSON format (no markdown, no explanation):
[
  {{"start": 10, "end": 50, "title": "Opening Hook", "reason": "Strong introduction"}},
  {{"start": 60, "end": 110, "title": "Main Point", "reason": "Key insight"}},
  {{"start": 120, "end": 170, "title": "Call to Action", "reason": "Ending message"}}
]"""
    
    try:
        if use_groq and groq_key:
            # Use Groq
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a viral content expert. Return ONLY valid JSON."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        else:
            # Use Gemini
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
            
    except Exception as e:
        return f'{{"error": "AI API Error: {str(e)}"}}'

def generate_blog_post(transcript, title, use_groq=True):
    """Generate blog post from transcript"""
    
    prompt_text = f"""Write a 400-word blog post about this video.

Video Title: {title}

Content:
{transcript[:3000]}

Include:
- Catchy headline
- 3-4 paragraphs
- Key takeaways"""
    
    try:
        if use_groq and groq_key:
            # Use Groq
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert content writer."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.8,
                max_tokens=800
            )
            return response.choices[0].message.content
        else:
            # Use Gemini
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
            
    except Exception as e:
        return f"Error generating blog: {str(e)}"