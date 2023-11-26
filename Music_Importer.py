import os
import shutil
from tinytag import TinyTag
from tqdm import tqdm

def clean_string(s):
    return str(s).replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip() if s is not None else ""

def import_metadata(directory="."):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a')):
                audio_path = os.path.join(root, file)
                audio = TinyTag.get(audio_path)
                audio_info = {
                    'Title_Track': clean_string(audio.title),
                    'Artist_Var': clean_string(audio.artist),
                    'Album_Var': clean_string(audio.album),
                    'full_path': os.path.join(root, file)
                }
                audio_files.append(audio_info)

    if not audio_files:
        print("No audio files found in the specified directory or its subdirectories.")
        exit()

    return audio_files

def make_and_move(audio_info):
    file_base = os.path.basename(audio_info['full_path'])
    _, file_extension = os.path.splitext(file_base)

    artist_var = clean_string(audio_info['Artist_Var'])
    album_var = clean_string(audio_info['Album_Var'])
    title_track = clean_string(audio_info['Title_Track'])

    default_file = "Unknown File"
    default_album = "Unknown Album"
    default_artist = "Unknown Artist"

    full_path = os.path.join(artist_var, album_var, f"{title_track}{file_extension}")

    try:
        if all(value == '' for value in audio_info.values()):
            tqdm.write(f"Skipping file with no metadata: {audio_info['full_path']}")
            return

        if artist_var and album_var:
            full_path = os.path.join(artist_var, album_var, f"{title_track}{file_extension}")

            if not os.path.exists(os.path.join(artist_var, album_var)):
                os.makedirs(os.path.join(artist_var, album_var))

            if audio_info['Artist_Var'] == '':
                shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))
            elif audio_info['Album_Var'] == '':
                shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))
            elif audio_info['Title_Track'] == '':
                shutil.move(audio_info['full_path'], os.path.join(artist_var, album_var, f"{default_file}{file_extension}"))
            elif os.path.exists(audio_info['full_path']):
                shutil.move(audio_info['full_path'], full_path)
                tqdm.write(f"{title_track} moved successfully to {full_path}")
            else:
                print(f"Error: Source file not found - {audio_info['full_path']}")
        else:
            default_dir = None

            if artist_var and title_track:
                full_path = os.path.join(artist_var, default_album, f"{title_track}{file_extension}")
                default_dir = os.path.join(artist_var, default_album)
            elif album_var and title_track:
                full_path = os.path.join(default_artist, album_var, f"{title_track}{file_extension}")
                default_dir = os.path.join(default_artist, album_var)
            elif artist_var and album_var:
                full_path = os.path.join(artist_var, album_var, f"{default_file}{file_extension}")
                default_dir = os.path.join(artist_var, album_var)
            elif not artist_var and album_var and title_track:
                full_path = os.path.join(default_artist, default_album, f"{default_file}{file_extension}")
                default_dir = os.path.join(default_artist, default_album)
            
            if default_dir is not None and not os.path.exists(default_dir):
                os.makedirs(default_dir)

            if os.path.exists(audio_info['full_path']):
                shutil.move(audio_info['full_path'], full_path)
                tqdm.write(f"{title_track} moved successfully to {full_path}")
            else:
                print(f"Error: Source file not found - {audio_info['full_path']}")

    except FileNotFoundError:
        print(f"Error: Source file not found - {audio_info['full_path']}")

# Main execution
audio_files = import_metadata()
for audio_info in tqdm(audio_files, desc='Processing', unit='file'):
    make_and_move(audio_info)

