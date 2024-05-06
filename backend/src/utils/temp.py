import tempfile
import os

def create_temp_structure() -> str:
    temp_dir = tempfile.gettempdir()
    temp_dir = os.path.join(temp_dir, "ytmp3")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir
