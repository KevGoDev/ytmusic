import yt_dlp
from flask import Blueprint, request, send_file
from models.yt import Download
from utils.database import db_scope
from utils.temp import create_temp_structure

bp = Blueprint("yt", __name__, url_prefix="/yt/")

TMP_DIR = create_temp_structure()


def progress_hook(d):
    video_id = d['info_dict']['id']
    progress = d['downloaded_bytes'] / d['total_bytes'] * 100
    with db_scope() as db:
        dl = Download.get_by_id(db, video_id)
        if not dl: raise Exception(f"Download with id {video_id} not found")
        dl.progress = progress
        if d['status'] == 'finished':
            if dl.status != 'finished':
                dl.status = 'finished'
        if d['status'] == 'downloading':
            if dl.status != 'downloading':
                dl.status = 'downloading'
        db.commit()


@bp.get("/convert")
def convert_yt_to_mp3():
    youtube_video_id = request.args.get('id')
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TMP_DIR}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={youtube_video_id}', download=False)
        output_path = f"{TMP_DIR}/{info['title']}.mp3"
        ydl.download([f'https://www.youtube.com/watch?v={youtube_video_id}'])

    # # Create entry for video
    with db_scope() as db:        
        dl = Download.get_by_id(db, youtube_video_id)
        if not dl:
            dl = Download.create(db, youtube_video_id, info.get("title", "N-D"), output_path)
            db.commit()
