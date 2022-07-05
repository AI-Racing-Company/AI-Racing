# AI-Racing
This is a Project in which cars will learn to race on a Track.
# Usage
## Create Tracks
To create a track you have to run "main.py". This will open a window with a car drawn on it. By clicking with the left mouse button, a point for a line will be drawn. By clicking miltiple times, the track can be created. To end the track, click withhin 50 pixels of the first point.
## Control the car
After both lines are drawn, the car can be controlled via WASD. Also, the resetpoint of the car can be changed by pressing "R". the new resetpoint will be at the cursors position.
## Import/Export tracks
### main.py:
In the main file, you easily can export the track you created by pressing "E". This will save the track as "track.csv". It is advised to rename it afterwards so you don't accidentally overwrite it. By pressing "I", a track will be imported. This track can be chosen in the file, and to change it, you have to rerun the script.
### Neat_with_calculate.py
In this file, there are no key inputs. To chose which track should be imported, you have to change the name of the file in the functions "importTrack" and "initialImportTrack". In this script, the file can't be exported.
## AI
### Training
To train the AI, you have some options to chose from in the Neat_with_calculate file. These are variables you can change after the inputs.
#### train_AI
If you want the AI to learn, you have to set this variable to True. If you just want to replay a generation from a checkpoint, set it to False.
#### use_Gen
If you either want to continue training a checkpoint you already have, or you want to replay a specific generation, set this to True. Else, set it to False.
#### Gen_file
This variable is only important, if use_Gen is True. This is the string to the file of the NEAT-Checkpoint.
#### random_tracks
If you want the AI to drive on a random Map, set this to True. If you want it to drive on a specific track, set it to False.
#### use_track
This variable is only used when random_tracks is False. This is the number to the track you want to be loaded.
#### draw_net
This variable indicates if the Net of the last generation should be drawn.

