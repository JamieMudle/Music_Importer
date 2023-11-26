import os
import shutil
from tinytag import TinyTag
from tqdm import tqdm

# Function for finding metadata within audio files inside folders within the specified directory.
def import_metadata(directory="."):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file is an MP3 or M4A audio file
            if file.lower().endswith(('.mp3', '.m4a')):
                audio_path = os.path.join(root, file)
                audio = TinyTag.get(audio_path)
                
                # Clean up metadata and create a dictionary
                audio_info = {
                    'Title_Track': str(audio.title).replace("\x00", ""),
                    'Artist_Var': str(audio.artist).replace("\x00", ""),
                    'Album_Var': str(audio.album).replace("\x00", ""),
                    'full_path': os.path.join(root, file)
                }
                audio_files.append(audio_info)

    # If there are no audio files found
    if not audio_files:
        print("No audio files found in the specified directory or its subdirectories.")
        exit()

    return audio_files

# Function for making directories, renaming, and moving files.
def make_and_move(audio_files):
    for audio_info in tqdm(audio_files, desc='Processing', unit='file'):
        file_base = os.path.basename(audio_info['full_path'])
        _, file_extension = os.path.splitext(file_base)
        
        # Clean up metadata for directory and file naming
        artist_var = audio_info['Artist_Var'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()
        album_var = audio_info['Album_Var'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()
        title_track = audio_info['Title_Track'].replace("/", " ").replace("+", "and").replace(":", "-").replace("\x00", "").strip()

        # Set default file names
        default_file = "Unknown File"
        default_album = "Unknown Album"
        default_artist = "Unknown Artist"
        
        # Construct full path for tracks that have all metadata
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
                # Move and rename files with the specified path name and track title
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
            # Handle cases where album, artist, and title are missing or incomplete
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
            
            # Create default directory if it doesn't exist
            if default_dir is not None and not os.path.exists(default_dir):
                try:
                    os.makedirs(default_dir)
                except OSError as e:
                    print(f"Error creating directory: {default_dir}")
                    print(e)

            if os.path.exists(audio_info['full_path']):
                shutil.move(audio_info['full_path'], full_path)
                tqdm.write(f"{title_track} moved successfully to {full_path}")
            else:
                print(f"Error: Source file not found - {audio_info['full_path']}")

# Main execution
audio_files = import_metadata()
make_and_move(audio_files)

