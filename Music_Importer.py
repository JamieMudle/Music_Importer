import os
import shutil
from tinytag import TinyTag
from tqdm import tqdm

def import_metadata(directory="."):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a')):  
                audio_path = os.path.join(root, file)
                audio = TinyTag.get(audio_path)
                audio_info = {
                    'Title_Track': str(audio.title).replace("\x00", ""),
                    'Artist_Var': str(audio.artist).replace("\x00", ""),
                    'Album_Var': str(audio.album).replace("\x00", ""),
                    'full_path': os.path.join(root, file)
                }
                audio_files.append(audio_info)
    
    if not audio_files:
        print("No audio files found in the specified directory or its subdirectories.")
        exit()

    return audio_files

def make_and_move(audio_files):
    for audio_info in tqdm(audio_files, desc='Processing', unit='file'):
        file_base = os.path.basename(audio_info['full_path'])
        _, file_extension = os.path.splitext(file_base)
        artist_var = audio_info['Artist_Var'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()
        album_var = audio_info['Album_Var'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()
        title_track = audio_info['Title_Track'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()

        # Set default file name
        default_file = "Unknown File"

        full_path = os.path.join(artist_var, album_var, f"{title_track}{file_extension}")

        if artist_var and album_var:
            full_path = os.path.join(artist_var, album_var, f"{title_track}{file_extension}")

            if not os.path.exists(os.path.join(artist_var, album_var)):
                try:
                    os.makedirs(os.path.join(artist_var, album_var))
                except OSError as e:
                    print(f"Error creating directory: {os.path.join(artist_var, album_var)}")
                    print(e)

            if all(value == '' for value in audio_info.values()):
                tqdm.write(f"Skipping file with no metadata: {audio_info['full_path']}")
            else:
                # Continue with the rest of the move logic
                if audio_info['Artist_Var'] == '':
                    shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))

                elif audio_info['Album_Var'] == '':
                    try:
                        shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))
                    except FileNotFoundError as e:
                        print(f"Error moving file: {e}")

                elif audio_info['Title_Track'] == '':
                    shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))

                elif os.path.exists(audio_info['full_path']):
                    shutil.move(audio_info['full_path'], full_path)
                    tqdm.write(f"{title_track} moved successfully to {full_path}")
                else:
                    print(f"Error: Source file not found - {audio_info['full_path']}")
        else:
            # Handle the case where the album is missing but the artist and title are present
            if artist_var and title_track:
                full_path = os.path.join(artist_var, default_file, f"{title_track}{file_extension}")

                if not os.path.exists(os.path.join(artist_var, default_file)):
                    try:
                        os.makedirs(os.path.join(artist_var, default_file))
                    except OSError as e:
                        print(f"Error creating directory: {os.path.join(artist_var, default_file)}")
                        print(e)

                if os.path.exists(audio_info['full_path']):
                    shutil.move(audio_info['full_path'], full_path)
                    tqdm.write(f"{title_track} moved successfully to {full_path}")
                else:
                    print(f"Error: Source file not found - {audio_info['full_path']}")

audio_files = import_metadata()
make_and_move(audio_files)

        
