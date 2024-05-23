from typing import Optional
import yt_dlp
from flask import Blueprint, request, send_file
from models.yt import Download
from utils.database import db_scope
from utils.temp import create_temp_structure
from dataclasses import dataclass
import logging
import boto3
import os
s3 = boto3.client(
    's3', 
    region_name='us-east-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
BUCKET = "ytmp3-uploaded-files"

bp = Blueprint("yt", __name__, url_prefix="/yt/")

TMP_DIR = create_temp_structure()

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'restrictfilenames': True,
    'outtmpl': f'{TMP_DIR}/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'force_generic_extractor': True,
    'dump_single_json': True,
}


@dataclass
class DownloadJobInfo:
    id: str
    title: str
    thumbnail: str


def create_video_job(video_id: str) -> DownloadJobInfo:
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
        # get output filename
        title = info['title'] or 'untitled'        
        thumbnail = info['thumbnail']
        # Create entry for video
        with db_scope() as db:
            dl = Download.get_by_id(db, video_id)
            if not dl:
                dl = Download.create(db, video_id, title)
                db.commit()
    return DownloadJobInfo(video_id, title, thumbnail)


def create_playlist_jobs(playlist_id: str, video_id: Optional[str]=None) -> list[DownloadJobInfo]:
    jobs = []
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        if playlist_id.startswith('RD'):
            url = f'https://www.youtube.com/watch?list={playlist_id}&v={video_id}'
        else:
            url = f'https://www.youtube.com/playlist?list={playlist_id}'
        info = ydl.extract_info(url, download=False)
        with db_scope() as db:
            if 'entries' not in info:
                logging.warning("+++++++++++++ No entries found in playlist +++++++++++++")
                for k in info.keys():
                    logging.warning(f"{k}: {info[k]}")
            for entry in info['entries']:
                video_id = entry['id']
                title = entry['title']
                thumbnail = None
                if 'thumbnail' in entry.keys():
                    thumbnail = entry['thumbnail']
                elif 'thumbnails' in entry.keys():
                    thumbnail = entry['thumbnails'][0]['url']
                jobs.append(DownloadJobInfo(video_id, title, thumbnail))
                dl = Download.get_by_id(db, video_id)
                if not dl:
                    dl = Download.create(db, video_id, title)
            db.commit()
    return jobs


@bp.get("/convert")
def convert_yt_to_mp3():
    youtube_video_id = request.args.get('id')
    youtube_playlist_id = request.args.get('list')
    if youtube_playlist_id:
        jobs = create_playlist_jobs(youtube_playlist_id, youtube_video_id)
    else:
        jobs = [create_video_job(youtube_video_id)]
    return {"jobs": jobs}


@bp.get("/status")
def get_download_status():
    youtube_video_id = request.args.get('id')
    with db_scope() as db:
        dl = Download.get_by_id(db, youtube_video_id)
        if not dl:
            return {"error": "Download not found"}, 404
        return {"status": dl.status, "progress": float(dl.progress)}


@bp.get("/download")
def download_yt_mp3():
    youtube_video_id = request.args.get('id')
    with db_scope() as db:
        dl = Download.get_by_id(db, youtube_video_id)
        if not dl:
            return {"error": "Download not found"}, 404
        if dl.status != 'finished':
            return {"error": "Download not finished"}, 400
        response = s3.generate_presigned_url(
            'get_object', 
            Params={
                'Bucket': BUCKET,
                'Key': dl.s3_key
            },
            ExpiresIn=3600*24
        )
        return {"url": response}
