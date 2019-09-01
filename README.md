# AtlaNET

### About
AtlaNet is a network of systems working together to retrieve, store and provide P2000 alerts.\
\
![Example](https://jkctech.nl/projects/atlan/cdn/github/example.jpg)

### Honorable Mentions
 - [1 FLEX Radio Tutorial | Richard IJzermans](https://raspberrytips.nl/p2000-meldingen-ontvangen/)
 - [2 Starter Code | oneguyoneblog](https://nl.oneguyoneblog.com/2016/08/09/p2000-ontvangen-decoderen-raspberry-pi/)
 - [3 Capcode Database Provider | Tom_Zulu](https://www.tomzulu10capcodes.nl/)

## Requirements
### Hardware
 - RTL2832U USB TV / Radio receiver (Aliexpress +- €10,-)
 - Raspberry Pi (Or some other Linux capable computer with USB)
 - Strobe Light (Optional + Requires soldering skills)
 - Arduino Nano (Optional for controlling the strobe light)


### Software
 - Python 2.7 (Specifically 2.7)
 - Pip (See requirements.txt for all the packages)
 - alsa alsa-tools (For volume management)
 - espeak (For the talking)
 - cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev qt4-default (For the radio, see link 1 in "Honorable Mentions")