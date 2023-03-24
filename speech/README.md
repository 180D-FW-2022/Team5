# Speech 
This is where all of our speech pipeline code lives

## Overview of files and subdirectories

### Hey-Edward\_en\_mac\_v2\_1\_0/ and Hey-Edward\_en\_raspberry\_pi\_v2\_1\_0/ 
Houses the "Hey Edward" pvporcupine wakeword models for the mac platform and raspberry pi platforms respectively

### hotkey.py
Runs the hotword recognition model leveraging pyporcupine. This is a low resource, high accuracy thread that rnus in the background and triggers the rest of the speech recognition system when it detects 
a relevant phrase

### SpeechDetector.py
`detect_speech()` is started by `hotkey.py` and invokes the Google Speech API to process our more complex voice commands

### StateArbitrator.py
`SpeechDetector.py` passes recognized commands to this class, which handles interfacing with relevant systems like the speaker and LEDs and main controller to act on the processed command

### speechmap.json
Maps every command to an index for internal convenience
