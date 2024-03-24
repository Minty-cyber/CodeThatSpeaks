import pyttsx3 as speech


engine = speech.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak_with_window_open():
    engine.say("Welcome to a demo page of the BasicLingua app!")
    engine.runAndWait()
