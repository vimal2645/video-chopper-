# 🎬 Viral Video Chopper

**Pixii.ai Founding Engineer Assignment**  
**By:** Vimal Prakash 

Turn any YouTube video into viral clips + SEO blog posts using AI in one click.

---

## 🎯 Problem It Solves

Content creators spend hours manually editing videos and writing blogs. This tool automates both in **under 2 minutes**.

---

## ✨ Features

- 📥 Download any YouTube video automatically
- 🤖 AI finds 3-5 viral moments (30-60 seconds each)
- ✂️ Auto-cuts clips with smart timestamps
- 📝 Generates SEO-optimized blog post
- 🎚️ Choose between Groq (faster) or Gemini AI
- 💾 Download clips and blog posts
- 🚀 Clean, minimal UI built with Streamlit

---

## 🛠️ Tools & APIs Used

1. **YouTube Data API** - Video download and metadata extraction
2. **Groq API (Llama 3.3 70B)** - Fast AI analysis and content generation
3. **Google Gemini 2.5 Flash** - Alternative AI model option
4. **MoviePy** - Video editing and clip cutting
5. **Streamlit** - Interactive web interface
6. **yt-dlp** - Robust YouTube video extraction

---

## 🚀 Quick Start (5 Steps)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/viral-video-chopper.git
cd viral-video-chopper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get FREE API keys
- **Groq API**: https://console.groq.com/ (sign up, create API key)
- **Gemini API**: https://aistudio.google.com/app/apikey (get API key)
- **youtube API** 
### 4. Create `.env` file and add your keys
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser and start generating clips!

---


