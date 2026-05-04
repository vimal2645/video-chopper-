import streamlit as st
import os
import shutil
from video_processor import cut_video, create_demo_video
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
st.markdown("**AI-powered video clip generator for content creators**")

st.info("💡 **Note:** Due to YouTube's 2026 bot protection, please upload your video file or use demo mode.")

# Mode selection
mode = st.radio(
    "Choose input mode:",
    ["📤 Upload Video", "🎬 Demo Mode"],
    horizontal=True
)

col1, col2 = st.columns([3, 1])

if mode == "📤 Upload Video":
    with col1:
        uploaded_file = st.file_uploader(
            "Upload video file (MP4, MOV, AVI)",
            type=['mp4', 'mov', 'avi', 'mkv']
        )
        video_description = st.text_area(
            "Describe your video (helps AI find viral moments):",
            placeholder="Example: This video is about landing tech internships, focusing on resume tips and interview strategies...",
            height=100
        )
else:
    with col1:
        video_description = st.text_area(
            "Describe the video content:",
            placeholder="Example: Career advice video about landing internships with resume tips and networking strategies...",
            height=100,
            value="This is a 5-minute career advice video covering: (1) How to optimize your resume for ATS systems, (2) Networking strategies on LinkedIn, (3) Common interview mistakes to avoid, (4) Salary negotiation tips, and (5) Building your personal brand."
        )

with col2:
    ai_model = st.selectbox(
        "AI Model:",
        ["Groq (Faster)", "Gemini (Google)"],
        help="Choose AI for analysis"
    )

use_groq = ai_model.startswith("Groq")

if st.button("🚀 Generate Clips & Blog", type="primary"):
    
    # Validation
    if mode == "📤 Upload Video" and not uploaded_file:
        st.error("Please upload a video file")
    elif not video_description:
        st.error("Please describe your video")
    else:
        try:
            cleanup_folders()
            
            # Handle video
            if mode == "📤 Upload Video":
                with st.spinner("📥 Processing uploaded video..."):
                    video_path = "temp/video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    title = uploaded_file.name
                    st.success(f"✅ Uploaded: {title}")
            else:
                with st.spinner("🎬 Creating demo video..."):
                    video_path = create_demo_video()
                    title = "Demo Video - Career Advice"
                    st.success("✅ Demo video ready")
            
            transcript = f"Title: {title}\n\nContent: {video_description}"
            
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
st.caption("🎯 Built for Pixii.ai Founding Engineer Assignment")
st.caption("⚡ Tech Stack: Streamlit + AI (Groq/Gemini) + FFmpeg + Python")
st.caption("⚠️ YouTube downloads blocked in 2026 due to bot protection. Use upload or demo mode.")