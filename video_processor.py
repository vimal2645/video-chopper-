import yt_dlp
import os
import json
import re
import subprocess

def download_video(url):
    """Download video from YouTube"""
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'temp/video.%(ext)s',
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = 'temp/video.mp4'
        title = info.get('title', 'video')
        duration = info.get('duration', 0)
        
    return video_path, title, duration

def get_transcript(url):
    """Get video description"""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        description = info.get('description', 'No description')
        title = info.get('title', '')
        return f"Title: {title}\n\nDescription: {description[:1000]}"

def cut_video(video_path, clips_data):
    """Cut video into clips using ffmpeg"""
    try:
        if isinstance(clips_data, str):
            clips_data = clips_data.strip()
            if clips_data.startswith('```'):
                clips_data = re.sub(r'```json?\s*|\s*```', '', clips_data)
            clips_data = json.loads(clips_data)
        
        clips = []
        os.makedirs('output/videos', exist_ok=True)
        
        # Use ./ffmpeg if exists, otherwise system ffmpeg
        ffmpeg_cmd = './ffmpeg' if os.path.exists('./ffmpeg') else 'ffmpeg'
        
        for i, clip in enumerate(clips_data, 1):
            start = clip.get('start', 0)
            end = clip.get('end', 30)
            title = clip.get('title', f'Clip {i}')
            reason = clip.get('reason', '')
            
            duration = end - start
            output_file = f'output/videos/clip_{i}.mp4'
            
            print(f"Creating clip {i}: {start}s to {end}s - {title}")
            
            cmd = [
                ffmpeg_cmd, '-y',
                '-ss', str(start),
                '-i', video_path,
                '-t', str(duration),
                '-c', 'copy',
                output_file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            clips.append({
                'file': output_file,
                'title': title,
                'reason': reason
            })
        
        return clips
        
    except Exception as e:
        print(f"Error: {e}")
        return []