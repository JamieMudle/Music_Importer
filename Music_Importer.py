#import modules for use.
import os
import shutil
from tinytag import TinyTag
from tqdm import tqdm

#import selected metadata from files iterating through directories.
def import_metadata(directory="."):
    global audio_files
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a')):  # Add more extensions as needed
                global audio_path
                audio_path = os.path.join(root, file)
                audio = TinyTag.get(audio_path)
                audio_info = {
                    'Title_Track': str(audio.title),
                    'Artist_Var': str(audio.artist),
                    'Album_Var': str(audio.album),
                    'full_path': os.path.join(root, file)
                }
                audio_files.append(audio_info)
    # error handling for empty directory
    if not audio_files:
        print("No audio files found in the specified directory or its subdirectories.")
        exit()

import_metadata()

# Make new directory based on artist and album if it doesn't exist already and move files there.
def make_and_move():
    for audio_info in tqdm(audio_files, desc='Processing', unit='file'):
        file_base = os.path.basename(audio_path)
        _, file_extension = os.path.splitext(file_base)
        artist_var = audio_info['Artist_Var'].replace("/", "_")
        album_var = audio_info['Album_Var'].replace("/", "_")
        title_track = audio_info['Title_Track'].replace("/", "_")
        full_path = os.path.join(artist_var, album_var, f"{title_track}{file_extension}")

        if not os.path.exists(os.path.join(artist_var, album_var)):
            os.makedirs(os.path.join(artist_var, album_var))
        
        shutil.move(audio_info['full_path'], full_path)
        tqdm.write(f"{title_track} moved successfully to {full_path}") # Print out progress as files are moved

make_and_move()




        
