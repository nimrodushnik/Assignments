I have data from a Pavlovian behavioral experiment, where each trial mice get a food reward after an odor cue.
The program that runs the experiment generates a .mat file with documentation of the mouse's licks.
I used copilot to create a python code that generates a raster plot of the licks.

prompt:
"I have a MATLAB `.mat` file containing data from an experiment where mice lick for a reward following an odor cue.
Each trial is stored as a separate structure and the licking data can be found in `TrialN.AnalogData.Button.Btn1`.
Write a simple Python script that:
1. Opens a file explorer window to select the `.mat` file.
2. Extracts lick events from each trial
3. Creates a lick raster plot with each trial on a separate row
4. Marks odor onset at 0 seconds and odor offset at 2 seconds with red dashed lines."
