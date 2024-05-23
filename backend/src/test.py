import yt_dlp
from utils.temp import create_temp_structure
TMP_DIR = create_temp_structure()

YDL_OPTIONS = {
    'extract_flat': True,
    'force_generic_extractor': True,
    'dump_single_json': True,
    'extractor_args': {'youtube:tab': {'flat': True}}
}

plist_mix = 'https://www.youtube.com/watch?v=e_S9VvJM1PI&list=RDMMe_S9VvJM1PI'
plist = 'https://www.youtube.com/watch?v=2EwViQxSJJQ&list=PL8629BA4D2BFD141B'

with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(plist_mix, download=False)
    for k in info.keys():
        print(f"{k}: {info[k]}")