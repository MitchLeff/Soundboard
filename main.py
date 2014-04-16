import winsound, random, time, math, datetime, os, string, wave, pymedia.audio.sound as sound

ROOT_DIR = "C:/Users/Mitch/Google Drive/Programming Stuff/Python/workspace/Soundboard/"


def playFile(filename):
	f = wave.open( filename, 'rb' )
	sampleRate= f.getframerate()
	channels= f.getnchannels()

	format = sound.AFMT_S16_LE

	snd= sound.Output( sampleRate, channels, format, 0)
	snd2= sound.Output( sampleRate, channels, format, 2)
	s= f.readframes( 300000 )
	snd.play( s )
	snd2.play( s )
	
	while snd2.isPlaying() or snd2.isPlaying(): 
		time.sleep( 0.05 )


class SoundClip:
    def __init__(self, filename, category = None):
        self.filename = filename
        self.category = category

    def play(self):
        print ROOT_DIR + str(self.category.name) + "/" + str(self.filename)
        playFile(ROOT_DIR + str(self.category.name) + "/" + str(self.filename))
		#winsound.PlaySound(ROOT_DIR + str(self.category.name) + "/" + str(self.filename), winsound.SND_FILENAME)
        #print self.filename
        #winsound.PlaySound(self.filename, winsound.SND_FILENAME)

class Category:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, clip):
        self.members.append(clip)

    def playRandomClip(self):
        random.choice(self.members).play()


cat1 = Category("cat1")
cat2 = Category("cat2")
for i in os.listdir(ROOT_DIR+cat1.name):
    cat1.add(SoundClip(i, cat1))

for i in os.listdir(ROOT_DIR+cat2.name):
    cat2.add(SoundClip(i, cat2))

import ctypes
from ctypes import wintypes
import win32con#

byref = ctypes.byref
user32 = ctypes.windll.user32

HOTKEYS = {
  1 : (win32con.VK_F3, win32con.MOD_SHIFT),
  2 : (win32con.VK_F4, win32con.MOD_SHIFT),
    }

HOTKEY_ACTIONS = {
  1 : cat1.playRandomClip,
  2 : cat2.playRandomClip,
}

for id, (vk, modifiers) in HOTKEYS.items ():
  print ("Registering id", id, "for key", vk)
  if not user32.RegisterHotKey (None, id, modifiers, vk):
    print ("Unable to register id", id)

try:
  msg = wintypes.MSG ()
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    if msg.message == win32con.WM_HOTKEY:
      action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      #print(" msg.message == win32con.WM_HOTKEY:")
      if action_to_take:
        action_to_take ()

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))

finally:
  for id in HOTKEYS.keys ():
    user32.UnregisterHotKey (None, id)
    print("user32.UnregisterHotKey (None, id)")