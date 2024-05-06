import yt_dlp
from flask import Blueprint, request, send_file
from models.yt import Download
from utils.database import db_scope
from utils.temp import create_temp_structure
import logging
import os

bp = Blueprint("yt", __name__, url_prefix="/yt/")

TMP_DIR = create_temp_structure()


def progress_hook(d):
    video_id = d['info_dict']['id']
    progress = d['downloaded_bytes'] / d['total_bytes'] * 100
    with db_scope() as db:
        dl = Download.get_by_id(db, video_id)
        if not dl: raise Exception(f"Download for id {video_id} not found")
        dl.progress = progress
        if d['status'] == 'finished':
            if dl.status != 'finished':
                dl.status = 'finished'
        if d['status'] == 'downloading':
            if dl.status != 'downloading':
                dl.status = 'downloading'
        db.commit()


@bp.get("/download")
def download_yt_mp3():
    youtube_video_id = request.args.get('id')
    with db_scope() as db:
        dl = Download.get_by_id(db, youtube_video_id)
        if not dl:
            return {"error": "Download not found"}, 404
        if dl.status != 'finished':
            return {"status": dl.status, "progress": dl.progress}
        return send_file(dl.path, as_attachment=True, download_name=f"{dl.title}.mp3")


@bp.get("/convert")
def convert_yt_to_mp3():
    youtube_video_id = request.args.get('id')
    options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
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
        # get output filename
        title = info['title'] or 'untitled'
        output_path = os.path.splitext(ydl.prepare_filename(info))[0] + '.mp3'
        # Create entry for video
        with db_scope() as db:        
            dl = Download.get_by_id(db, youtube_video_id)
            if not dl:
                dl = Download.create(db, youtube_video_id, title, output_path)
                db.commit()
        ydl.download([f'https://www.youtube.com/watch?v={youtube_video_id}'])
    return send_file(output_path, as_attachment=True, download_name=f"{os.path.basename(output_path)}.mp3")
