import os
import shutil
from tinytag import TinyTag
def import_metadata():
    global enter_track
    enter_track = input("Please enter track here: ")
    audio = TinyTag.get(enter_track)
    global Title_Track
    global Artist_Var
    global Album_Var
    Title_Track = audio.title
    Artist_Var = audio.albumartist
    Album_Var = audio.album
    

    
import_metadata()
    
def Make_and_move():

    enter_track_base = os.path.basename(enter_track)
    _, file_extension = os.path.splitext(enter_track_base)
    full_path = os.path.join(Artist_Var, Album_Var, f"{os.path.basename(enter_track)}")

    if not os.path.exists(os.path.join(Artist_Var, Album_Var)):
        os.makedirs(os.path.join(Artist_Var, Album_Var))
        shutil.move(enter_track, full_path)
        print(f"Directory {Artist_Var}/{Album_Var} create. {Title_Track} moved inside")
        
    else:
        shutil.move(enter_track, full_path)
        print(f"{Title_Track} moved successfully")
Make_and_move()



        