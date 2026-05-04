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
    """Get video transcript/description"""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        # Try to get subtitles first
        if info.get('subtitles') or info.get('automatic_captions'):
            subs = info.get('subtitles', {}).get('en') or info.get('automatic_captions', {}).get('en')
            if subs:
                return f"Title: {info.get('title')}\nDescription: {info.get('description', '')[:500]}"
        
        # Fallback to description
        description = info.get('description', 'No description available')
        title = info.get('title', '')
        return f"Title: {title}\n\nDescription: {description}"

def cut_video(video_path, clips_data):
    """Cut video into clips using ffmpeg"""
    try:
        # Parse JSON if it's a string
        if isinstance(clips_data, str):
            clips_data = clips_data.strip()
            if clips_data.startswith('```'):
                clips_data = re.sub(r'```json?\s*|\s*```', '', clips_data)
            clips_data = json.loads(clips_data)
        
        clips = []
        os.makedirs('output/videos', exist_ok=True)
        
        for i, clip in enumerate(clips_data, 1):
            start = clip.get('start', 0)
            end = clip.get('end', 30)
            title = clip.get('title', f'Clip {i}')
            reason = clip.get('reason', '')
            
            duration = end - start
            output_file = f'output/videos/clip_{i}.mp4'
            
            print(f"Creating clip {i}: {start}s to {end}s - {title}")
            
            # Use ffmpeg command
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start),
                '-i', video_path,
                '-t', str(duration),
                '-c', 'copy',
                output_file
            ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                clips.append({
                    'file': output_file,
                    'title': title,
                    'reason': reason
                })
            except subprocess.CalledProcessError as e:
                print(f"Error creating clip {i}: {e}")
                continue
        
        return clips
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return []
    except Exception as e:
        print(f"Error cutting video: {e}")
        return []