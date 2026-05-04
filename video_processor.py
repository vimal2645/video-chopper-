import os
import json
import re
import subprocess

def create_demo_video():
    """Create a 5-minute demo video"""
    try:
        import imageio_ffmpeg as ffmpeg
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    except:
        ffmpeg_exe = 'ffmpeg'
    
    output_path = 'temp/video.mp4'
    
    cmd = [
        ffmpeg_exe, '-y',
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

def cut_video(video_path, clips_data):
    """Cut video into clips using ffmpeg"""
    try:
        import imageio_ffmpeg as ffmpeg
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    except:
        ffmpeg_exe = 'ffmpeg'
    
    try:
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
            
            cmd = [
                ffmpeg_exe, '-y',
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