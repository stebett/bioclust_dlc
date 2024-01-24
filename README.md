# Deeplabcut Bioclust

## Prerequisites
#### What you must have done
- You must be on linux
- You must have a DLC project 
- You must have extracted and labeled some frames
- You must have copied the videos in the DLC project folder (it's a parameter in the *create_project* function)
- You must have installed rsync 
- You may have to set up no-password connection to jord and bioclust

## Instructions
#### What do you have to do
- Clone this repository
- Update task script if needed with specifications (video names, ram to ask to bioclust, etc)
- Run the program
- Insert the project config path
- Insert working directory on the cluster ("e.g. /kingdoms/nbc/workspace12/yourname/)
- Select task (dlc function to perform)

## Functioning
#### What will the program do
- Copy your project on the cluster (with rsync --update, so no overwriting)
- Modify the project path of dlc so that it corresponds to the cluster position
- Change the project path on the python script for the task you selected
- Submit the task on bioclust (gpu)
- Show you the stderr output off the process
- Returns you the terminal once the process finished


## Problems
- Sometimes bioclusts likes to kick you from the server, especially if you are not on the same network
