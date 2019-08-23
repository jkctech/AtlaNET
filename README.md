# AtlaNET

### About
AtlaNet is a network of systems working together to retrieve, store and provide P2000 alerts.\
This project is based on oneguyoneblog's code found [here](https://nl.oneguyoneblog.com/2016/08/09/p2000-ontvangen-decoderen-raspberry-pi/).\
This project is based on a tutorial on setting-up the RPI FLEX radio found [here](https://raspberrytips.nl/p2000-meldingen-ontvangen/).

### Monitor:
![Example](https://jkctech.nl/projects/atlan/cdn/github/example.jpg)

### Changelog:
23-08-2019
 - Fixed speaker speed
 - Added quick debug speaker to custom need
 - Added 2 quick ways to save data to a log file

18-08-2019
 - Added text to speach (TTS) controller

08-08-2019
 - Minor changes to the monitor script
 - Introduction of the filter script (will replace parts of the code in monitor.py)
 - Preparations for planned features including logging, caching and saving.

01-08-2019
 - Renamed p2000.py > monitor.py
 - Added config files (Rename config_default.json to config.json for proper usage)
 - Created web connector to send the messages to the server
 - Removed error log file code entirely

31-07-2019
 - Initial creation / adaptation of original code