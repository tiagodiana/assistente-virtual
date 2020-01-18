from gtts import gTTS
from io import BytesIO
from playsound import playsound

my_variable = 'hello' # your real code gets this from the chatbot
 
mp3_fp = BytesIO()
tts = gTTS(my_variable)
tts.write_to_fp(mp3_fp)

import musicplayer
class Song:
    def __init__(self, f):
        self.f = f
    def readPacket(self, size):
        return self.f.read(size)
    def seekRaw(self, offset, whence):
        self.f.seek(offset, whence)
        return f.tell()
player = musicplayer.createPlayer()
player.queue = [Song(mp3_fp)]
player.playing = True