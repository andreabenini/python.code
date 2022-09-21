# 5 min TTS with python (courtesy of Google)
Installing required packages
```sh
pip install gTTS
```
and now some TTS
```python
from gtts import gTTS
import os
myobj = gTTS(text='Python and TTS in 5 minutes', lang='en', slow=False)
myobj.save("somespeech.mp3")
```

# pyttsx3 alternative
```sh
pacman -Ss espeakup
#...or whatever package installer command for providing 'libespeak.so.1' to your system

# this is a wrapper around libespeak.so.1
pip install pyttsx3
```
and python...
```python
import pyttsx3
engine = pyttsx3.init()
engine.say('less than 5 minutes this time')
engine.runAndWait()
```
