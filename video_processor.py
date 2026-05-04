import yt_dlp
import os
import json
import re
import subprocess


def create_demo_video():
    """Create a 5-minute demo video"""
    output_path = 'temp/video.mp4'
    
    # Use ./ffmpeg if exists, otherwise system ffmpeg
    ffmpeg_cmd = './ffmpeg' if os.path.exists('./ffmpeg') else 'ffmpeg'
    
    # Create a simple test video
    cmd = [
        ffmpeg_cmd, '-y',
        '-f', 'lavfi',
        '-i', 'color=c=blue:s=1280x720:d=300',
        '-f', 'lavfi',
        '-i', 'anullsrc=r=44100:cl=stereo',
        '-t', '300',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
def download_video(url):
    """Download video from YouTube with bot protection bypass"""
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'temp/video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        # Add headers to avoid bot detection
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        # Bypass age restriction and bot checks
        'age_limit': None,
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_client': ['android', 'web']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = 'temp/video.mp4'
            
            # Handle downloaded file extension
            if not os.path.exists(video_path):
                # Find the actual downloaded file
                for file in os.listdir('temp'):
                    if file.startswith('video.'):
                        os.rename(f'temp/{file}', video_path)
                        break
            
            title = info.get('title', 'video')
            duration = info.get('duration', 0)
            
        return video_path, title, duration
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def get_transcript(url):
    """Get video description"""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            description = info.get('description', 'No description')
            title = info.get('title', '')
            return f"Title: {title}\n\nDescription: {description[:1000]}"
    except Exception as e:
        return f"Title: Video\n\nDescription: Could not fetch description. Error: {str(e)}"

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