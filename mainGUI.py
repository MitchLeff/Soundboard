import winsound, random, time, math, datetime, os, string, wave, ctypes, win32con, Tkinter as TK, pymedia.audio.sound as sound, thread, threading
from ctypes import wintypes

ROOT_DIR = "../Categories/"
BOARD_WIDTH= 16


class SoundClip:
    clips = []
    stop = False
    
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
        #snd= sound.Output( sampleRate, channels, format, 0) #Speakers
        snd= sound.Output( sampleRate, channels, format, 0) #Virtual Cable
        s= f.readframes( 10000000 )
        
        snd.play( s )
        

        while snd.isPlaying():
            if SoundClip.stop:
                lock = threading.Lock()
                lock.acquire()
                SoundClip.stop = False
                lock.release()
                break
            else:
                continue
	
        
    def threadPlay(self):
        thread.start_new_thread(self.play, ())

    def playRandomClip(self):
        random.choice(SoundClip.clips).threadPlay()
        
    def stopClip(self):
        SoundClip.stop = True
        
class Category:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, clip):
        self.members.append(clip)

    def playRandom(self):
        random.choice(self.members).threadPlay()

class App:
	def __init__(self, master):
                self.master = master
		TK.Button(master, text="QUIT", fg="red", bg="green", command=self.master.quit).grid(row=0,column=0)
		TK.Button(master, text="RANDOM", fg="blue", bg="green", command=SoundClip.clips[0].playRandomClip).grid(row=0,column=1)
		TK.Button(master, text="STOP", fg="yellow", bg="green", command=reset).grid(row=0,column=2)
		
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
		

def reset():
    root= TK.Tk()
    app = App(root)

    cumVertOffset= 0 #when a row exceeds the max length, this is incremented to be added to the rows of the proceeding categories/clips.
    for m, cat in enumerate(categories, 1):
        #Create buttons
        TK.Button(root, text=cat.name, command = cat.playRandom, height = 1, width = 10, activebackground="red", anchor=TK.W).grid(row=m+cumVertOffset, column=0)
        for n, clip in enumerate(cat.members, 1):
            TK.Button(root, text=clip.filename[:-4], command=clip.threadPlay, height = 1, width = 15, justify=TK.LEFT, activebackground="red", anchor=TK.W, highlightbackground="green").grid(row=m+cumVertOffset, column=n%BOARD_WIDTH+1	)
            if not n%BOARD_WIDTH:
                cumVertOffset += 1

    root.mainloop()
    root.destroy()

reset()

#HOTKEYS

# byref = ctypes.byref
# user32 = ctypes.windll.user32


# HOTKEYS = {}
    
# HOTKEY_ACTIONS = {}

# for i in range(0, len(categories)):
    # HOTKEYS[i] = (i+65, win32con.MOD_ALT)
    # HOTKEY_ACTIONS[i] = categories[i].playRandomClip
    # print categories[i].name + " : Alt + " + chr(i+65)


# for id, (vk, modifiers) in HOTKEYS.items ():
  # print ("Registering id", id, "for key", vk)
  # if not user32.RegisterHotKey (None, id, modifiers, vk):
    # print ("Unable to register id", id)
    


# try:
  # msg = wintypes.MSG ()
  # while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    # if msg.message == win32con.WM_HOTKEY:
      # action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      # if action_to_take:
        # action_to_take ()

    # user32.TranslateMessage (byref (msg))
    # user32.DispatchMessageA (byref (msg))

# finally:
  # for id in HOTKEYS.keys ():
    # user32.UnregisterHotKey (None, id)
    # print("user32.UnregisterHotKey (None, id)")
