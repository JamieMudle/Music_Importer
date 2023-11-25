#Music_Importer

----------------Description------------------------------------------------------------------------------

This is a simple file in python for organizing music based on metadata. 
It works by iterating through the directory it is placed in plus any child directories, finding the audio files with the extensions passed into .endswith within the program (currently only .mp3 and .m4a)
once it finds the files it reads the metadata and then cretes directories for the artist, inside that directory it'll make an album directory and then rename the file with the title of the track and place it inside. 

If the directory for either artist or album exsists it should place the renamed files inside the appropriate directory. If there are no files ending in .mp3 or .m4a in the directory it will produce a message to inform you of this. 

----------------------------------Installation-----------------------------------------------------------

Clone the repository down
Install python in whichever way is appropriate for your OS
pip install tinytag and tqdm 
move the Music_Importer.py file into the parent directory you'd like to work with. 
run the program with python Music_Importer.py or python3 Music_Importer.py

---------------------------------Contact-----------------------------------------------------------------

If there are any issues please let me know!

