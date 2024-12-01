from cmu_graphics import *
from pathlib import Path
from PIL import Image

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
plants_dir = media_dir / "plants_gifs"
pea_dir = plants_dir / "peashooter.gif"
output_dir = plants_dir / "peashooter"
output_dir.mkdir(exist_ok=True)

def extract_frames(gif_path, output_dir):
    with Image.open(gif_path) as img:
        frame_index = 0
        while True:
            frame_path = output_dir / f"frame_{frame_index:02}.png"
            img.save(frame_path)
            frame_index += 1
            try:
                img.seek(frame_index) 
            except EOFError:
                break 

extract_frames(pea_dir, output_dir)