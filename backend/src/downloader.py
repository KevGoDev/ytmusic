import os
import time
import glob
from celery import Celery
from dotenv import load_dotenv
import yt_dlp

from utils.temp import create_temp_structure
from models.yt import Download
from utils.database import db_init, db_scope
import logging
import boto3
load_dotenv()

TMP_DIR = create_temp_structure()
app = Celery('tasks', broker=os.getenv('REDIS_URL'))
s3 = boto3.client(
    's3', 
    region_name='us-east-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
BUCKET = "ytmp3-uploaded-files"


def progress_hook(d):
    video_id = d['info_dict']['id']
    with db_scope() as db:
        dl = Download.get_by_id(db, video_id)
        if not dl: raise Exception(f"Download for id {video_id} not found")
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            dl.progress = d['downloaded_bytes'] / d['total_bytes'] * 100
        # Update status
        if d['status'] == 'finished':
            if dl.status != 'finished':
                dl.status = 'finished'
            # Upload to S3
            fname = dl.path
            if not fname:
                raise Exception(f"Path not found for download {dl.id}")
            if not os.path.exists(fname):
                raise Exception(f"File {fname} not found for download {dl.id}\n{glob.glob(TMP_DIR+'/*')}")
            with open(fname, 'rb') as f:
                s3_key = os.path.basename(fname)
                s3.upload_fileobj(f, BUCKET, s3_key)
                dl.s3_key = s3_key
        if d['status'] == 'downloading':
            if dl.status != 'downloading':
                dl.status = 'downloading'
        db.commit()


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'restrictfilenames': True,
    'outtmpl': f'{TMP_DIR}/%(title)s.mp3',
    'progress_hooks': [progress_hook],
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


@app.task
def download_video(id: str):
    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={id}', download=False)
            # replace ext with .mp3
            output_path = os.path.splitext(ydl.prepare_filename(info))[0] + '.mp3'
            with db_scope() as db:
                dl = Download.get_by_id(db, id)
                dl.path = output_path
                db.commit()
            logging.warning(f"Downloading video with ID {id} to {output_path}")
            # Download progress and completion will be handled by progress_hook
            ydl.download([f'https://www.youtube.com/watch?v={id}'])
    except Exception as e:
        logging.exception(f"Error downloading video with ID {id}: {e}")
        with db_scope() as db:
            dl = Download.get_by_id(db, id)
            dl.status = 'error'
            db.commit()
        return


# Worker manager
def manager():
    db_init()
    ids = []
    while True:
        with db_scope() as db:
            tasks = Download.get_all_unstarted(db)
            for task in tasks:
                if task.id not in ids:
                    logging.warning(f"Scheduling task with ID {task.id}")
                    ids.append(task.id)
                    download_video.delay(task.id)
        time.sleep(1)


if __name__ == "__main__":
    # check if 'worker' is passed as argument in argv
    if os.environ.get('WORKER'):
        logging.warning("Starting worker")
        args = ['worker', '--loglevel=INFO']
        app.worker_main(argv=args)
    else:
        logging.warning("Starting manager")
        manager()
