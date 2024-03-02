import pyttsx3 as speech


engine = speech.init()


engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  


text = "I love python programming!"
engine.say(text)


engine.runAndWait()
