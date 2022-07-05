# AI-Racing
This is a Project in which cars will learn to race on a Track. It was created as a school project by me and Jibril6407.
# Usage
## Create Tracks
To create a track you have to run "main.py". This will open a window with a car drawn on it. By clicking with the left mouse button, a point for a line will be drawn. By clicking miltiple times, the track can be created. To end the track, click withhin 50 pixels of the first point.
## Control the car
After both lines are drawn, the car can be controlled via WASD. Also, the resetpoint of the car can be changed by pressing "R". the new resetpoint will be at the cursors position.
## Import/Export tracks
### main.py:
In the main file, you easily can export the track you created by pressing "E". This will save the track as "track.csv". It is advised to rename it afterwards so you don't accidentally overwrite it. Also, the name should be "track_x.csv", because the random loading is made by random number generation. By pressing "I", a track will be imported. This track can be chosen in the file, and to change it, you have to rerun the script.
### Neat_with_calculate.py
In this file, there are no key inputs. To chose which track should be imported, you have to change the name of the file in the functions "importTrack" and "initialImportTrack". In this script, the file can't be exported.
## AI
### Training
To train the AI, you have some options to chose from in the Neat_with_calculate file. These are variables you can change after the inputs.
- #### train_AI
- -  If you want the AI to learn, you have to set this variable to True. If you just want to replay a generation from a checkpoint, set it to False.
- #### use_Gen
- -  If you either want to continue training a checkpoint you already have, or you want to replay a specific generation, set this to True. Else, set it to False.
- #### Gen_file
- -  This variable is only important, if use_Gen is True. This is the string to the file of the NEAT-Checkpoint.
- #### numMaxGen
- - This variable is used to set the max amount of generations. For training, this should be set as high as possible. For printing the net, it is advised to set it to 1.
- #### random_tracks
- -  If you want the AI to drive on a random Map, set this to True. If you want it to drive on a specific track, set it to False.
- #### max_tracks
- -  If random_tracks is True, this variable is used for tha maximum number of Tracks
- #### change_prop
- -  If random_tracks is True, this variable is the possibility (1/x) of a new track after each generation.
- #### use_track
- -  This variable is only used when random_tracks is False. This is the number to the track you want to be loaded.
- #### draw_net
- -  This variable indicates if the Net of the last generation should be drawn. When it has been drawn, it is advised to rename the file it was saved to, since it will be overwritten if you run again.
- - NOTE: to use the visualization, you have to install [graphviz](https://graphviz.org/download/) and change the file do the bin folder in visualize.py
- #### POPULATION
- -  The amount of cars per generation. Has to be changed in "config-feedforward.txt" accordingly.
- #### maxTicks
- -  The amount of Ticks a generation has before being reset for next generation.
- #### increaseTicks
- -  The amount of Ticks added to maxTicks per generation.
- #### absMaxTicks
- -  The amount of Ticks at the absolute maximum, not being increased over time.
- #### calcTime
- -  Set this to True if you want to see the time it takes to run through on_update.

After setting up all these variables in a way you want, you can run the file.



## GUI
If you want to see the cars drive, you have to run the script "neat_GUI.py" as well.

# Technical Infos
## AI
The AI gets fed the distances to the tracks in five directions at a FOV of 180°. the Outputs are 4 values, each of which represents a boolean. If the output of the respective neuron is greater than 0.5, the output is True. These four outputs simulate the player key presses of WASD.

## GUI
Since we couldn't find a way to combine NEAT and our GUI, arcade, we had to think of another way. The script Neat_with_calculate.py writes the playerdata (x,y,rotation) into a CSV file, and neat_GUI reads this file and draws these cars. Due to this, the cars sometimes flicker.

# Sources (note: these are not all of them, just the more important ones)
- [NEAT]([https://www.google.com](https://neat-python.readthedocs.io/en/latest/))
- [NEAT tutorial Flappy bird](bit.ly/3bO3UdO)
- [NEAT tutorial car driving](https://www.youtube.com/watch?v=2o-jMhXmmxA&t=143s&ab_channel=CheesyAI)
- [arcade](https://api.arcade.academy/en/latest/)
