# Role Calculator for Football Manager 24

Original Idea can be found here: [https://squirrelplays.neocities.org](https://squirrelplays.neocities.org)
Youtube Video: [https://www.youtube.com/watch?v=hnAuOakqR90&t=189s](https://www.youtube.com/watch?v=hnAuOakqR90&t=189s)
Original Files: [https://www.mediafire.com/file/u8n2patg2n5vwno/FM24_files_and_code.zip/file](https://www.mediafire.com/file/u8n2patg2n5vwno/FM24_files_and_code.zip/file)
## Idea
For each role there are certain player attributes required, to have an idea which player can fit the desired role best this tool can be used. 

To calculate a score there are 3 types of attributes taken into account:
- Key attribute     - factor x5
- Green attributes  - factor x3
- Blue attributes   - factor x1

Key, green & blue attributes are summed up and divided by the number of attribues == Average is calculated. 
Higher numbers means the player is more suitable for the certain role

## Sequence
- Watch the Youtube video, the setup of the individual filter/views is very well explained
- Export the players to analyze from the scouting feed/panel as described in the video
- Execute the python script within this repo with the file path to the exported file as argument
- The script will check if the exported file contains the required data and calculate the values for all roles

## Installation / Run
- run `poetry install` to get all necessary dependencies
- activate environment with `poetry shell` 
- start script with `python3 role-score-calculator.py <file>`
- or run script directly with `poetry run python3 role-score-calculator.py <file>`

## Todo
- Add installation section to this README
- Find way to get along with attribute ranges (e.g. 6-11, instead of 8)
