import winsound, random, time, math, datetime, os, string, wave, ctypes, win32con, Tkinter as TK, pymedia.audio.sound as sound
from ctypes import wintypes

ROOT_DIR = "../Categories/"

class SoundClip:
    clips = []
    
    def __init__(self, filename, category = None):
        self.filename = filename
        self.category = category
        SoundClip.clips.append(self)

    def play(self):
        print self.filename

        f = wave.open( ROOT_DIR + str(self.category.name) + "/" + str(self.filename), 'rb' )
        sampleRate = f.getframerate()
        channels = f.getnchannels()

        format = sound.AFMT_S16_LE
        snd= sound.Output( sampleRate, channels, format, 2)
        s= f.readframes( 10000000 )
        
        snd.play( s )
        
        while snd.isPlaying():
            time.sleep( 0.05 )
    
class Category:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, clip):
        self.members.append(clip)

    def playRandomClip(self):
        random.choice(self.members).play()


#Create Categories
categories = []

#Go through each folder and make a category for each one        
for i in os.listdir(ROOT_DIR):
    currCat = Category(i)
    categories.append(currCat)
    
    #Go through each catagory and add the files to the catagory
    for j in os.listdir(ROOT_DIR+currCat.name):
        if j[-4:] == ".wav":
            currCat.add(SoundClip(j, currCat))

        
#HOTKEYS

byref = ctypes.byref
user32 = ctypes.windll.user32


HOTKEYS = {}
    
HOTKEY_ACTIONS = {}

for i in range(0, len(categories)):
    HOTKEYS[i] = (i+65, win32con.MOD_ALT)
    HOTKEY_ACTIONS[i] = categories[i].playRandomClip
    print categories[i].name + " : Alt + " + chr(i+65)


for id, (vk, modifiers) in HOTKEYS.items ():
  print ("Registering id", id, "for key", vk)
  if not user32.RegisterHotKey (None, id, modifiers, vk):
    print ("Unable to register id", id)
    


try:
  msg = wintypes.MSG ()
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    if msg.message == win32con.WM_HOTKEY:
      action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      if action_to_take:
        action_to_take ()

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))

finally:
  for id in HOTKEYS.keys ():
    user32.UnregisterHotKey (None, id)
    print("user32.UnregisterHotKey (None, id)")
