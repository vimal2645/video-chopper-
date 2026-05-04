import yt_dlp
import os
from moviepy.editor import VideoFileClip
import json
import re

def download_video(url, output_path="temp"):
    """Download YouTube video"""
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/video.mp4',
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Video')
        duration = info.get('duration', 0)
        
    return f'{output_path}/video.mp4', title, duration

def get_transcript(url):
    """Extract transcript from YouTube video"""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            description = info.get('description', '')
            title = info.get('title', '')
            
            transcript = f"Video Title: {title}\n\nDescription: {description}"
            
            return transcript[:3000]
    except Exception as e:
        return f"Could not extract transcript. Error: {str(e)}"

def cut_video(video_path, clips_data, output_dir="output/videos"):
    """Cut video into clips based on timestamps"""
    os.makedirs(output_dir, exist_ok=True)
    
    video = VideoFileClip(video_path)
    generated_clips = []
    
    try:
        # Handle both string and already-parsed data
        if isinstance(clips_data, str):
            clips_data = clips_data.strip()
            # Remove markdown code blocks if present
            if '```json' in clips_data:
                clips_data = clips_data.split('```json').split('```')[1]
            elif '```' in clips_data:
                clips_data = clips_data.split('```')[1].split('```')[0]
            
            clips = json.loads(clips_data)
        else:
            clips = clips_data
        
        # Ensure clips is a list
        if not isinstance(clips, list):
            print(f"Expected list, got: {type(clips)}")
            return generated_clips
        
        for i, clip in enumerate(clips[:5], 1):
            try:
                start = int(clip['start'])
                end = int(clip['end'])
                title = clip.get('title', f'Clip_{i}')
                
                # Validate timestamps
                if start < 0 or end <= start:
                    print(f"Skipping invalid timestamps: start={start}, end={end}")
                    continue
                
                if end > video.duration:
                    end = int(video.duration)
                
                # Clean title for filename
                safe_title = re.sub(r'[^\w\s-]', '', title).strip()[:30]
                safe_title = safe_title.replace(' ', '_')
                output_file = f"{output_dir}/clip_{i}_{safe_title}.mp4"
                
                print(f"Creating clip {i}: {start}s to {end}s - {title}")
                
                subclip = video.subclip(start, end)
                subclip.write_videofile(
                    output_file, 
                    codec='libx264', 
                    audio_codec='aac', 
                    logger=None,
                    preset='ultrafast'
                )
                subclip.close()
                
                generated_clips.append({
                    'file': output_file,
                    'title': title,
                    'reason': clip.get('reason', '')
                })
                
            except Exception as e:
                print(f"Error creating clip {i}: {e}")
                continue
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw data: {clips_data[:200]}")
    except Exception as e:
        print(f"Error cutting video: {e}")
    finally:
        video.close()
    
    return generated_clips