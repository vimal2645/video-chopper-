import streamlit as st
import os
import shutil
from video_processor import download_video, get_transcript, cut_video
from ai_helper import analyze_transcript, generate_blog_post

st.set_page_config(page_title="Viral Video Chopper", page_icon="🎬", layout="wide")

# Create directories
os.makedirs("temp", exist_ok=True)
os.makedirs("output/videos", exist_ok=True)
os.makedirs("output/blogs", exist_ok=True)

def cleanup_folders():
    """Clean temp and output folders"""
    folders = ['temp', 'output/videos', 'output/blogs']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

st.title("🎬 Viral Video Chopper")
st.markdown("Turn any YouTube video into viral clips + blog posts using AI")

# AI Model Selector
col1, col2 = st.columns([3, 1])
with col1:
    url = st.text_input("Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")
with col2:
    ai_model = st.selectbox(
        "AI Model:",
        ["Groq (Faster)", "Gemini (Google)"],
        help="Choose AI model for analysis"
    )

use_groq = ai_model.startswith("Groq")

if st.button("🚀 Generate Clips & Blog", type="primary"):
    if not url:
        st.error("Please enter a YouTube URL")
    else:
        try:
            cleanup_folders()
            
            with st.spinner("📥 Downloading video..."):
                video_path, title, duration = download_video(url)
                st.success(f"✅ Downloaded: {title} ({duration}s)")
            
            with st.spinner("📝 Extracting transcript..."):
                transcript = get_transcript(url)
                st.info(f"Transcript preview: {transcript[:200]}...")
            
            with st.spinner(f"🤖 AI analyzing viral moments ({ai_model})..."):
                clips_data = analyze_transcript(transcript, use_groq=use_groq)
                st.code(clips_data, language="json")
            
            with st.spinner("✂️ Cutting video clips..."):
                clips = cut_video(video_path, clips_data)
                st.success(f"✅ Generated {len(clips)} clips!")
            
            if len(clips) > 0:
                st.subheader("🎥 Generated Clips")
                for clip in clips:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.video(clip['file'])
                    with col2:
                        st.markdown(f"**{clip['title']}**")
                        st.caption(clip['reason'])
            
            with st.spinner(f"📄 Generating blog post ({ai_model})..."):
                blog = generate_blog_post(transcript, title, use_groq=use_groq)
                blog_path = "output/blogs/blog.md"
                with open(blog_path, 'w', encoding='utf-8') as f:
                    f.write(blog)
                st.success("✅ Blog post generated!")
            
            st.subheader("📝 Blog Post")
            st.markdown(blog)
            
            with open(blog_path, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="📥 Download Blog Post",
                    data=f.read(),
                    file_name="blog_post.md",
                    mime="text/markdown"
                )
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + AI (Groq/Gemini) + yt-dlp + MoviePy")