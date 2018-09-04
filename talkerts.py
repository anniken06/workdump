import pyttsx3  # pip install pyttsx3
import win32clipboard  # pip install pypiwin32

class Talker(object):
    def __init__(self, rate_offset = 50):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.engine.getProperty('rate') + rate_offset)
    
    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    
    def talk(self):
        data = self.get_clipboard()
        print("Saying: \n", data)
        self.engine.say(data)
        self.engine.runAndWait()

    def stop(self):
        print("Stopped talking...")
        self.engine.stop()


import keyboard  # pip install keyboard
import time

poll_time = 0.25
talker = Talker()
try:
    while True:
        if keyboard.is_pressed('t') and keyboard.is_pressed('s'):
            talker.talk()
        print("polling...")
        time.sleep(poll_time)
except Exception as e:
    print("Exception", e)
finally:
    del(talker)
