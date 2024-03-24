import pyttsx3 as speech


engine = speech.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak_with_window_open():
    engine.say("Welcome to a demo page of the BasicLingua app!")
    engine.runAndWait()
    
    
    
    
# self.username_input.installEventFilter(self)
#         self.password_input.installEventFilter(self)

#     # Define event filter method outside the class
#     def eventFilter(self, obj, event):
#         if event.type() == QEvent.FocusIn:
#             obj.setStyleSheet("border: 2px solid red; border-radius: 5px;")
#         elif event.type() == QEvent.FocusOut:
#             obj.setStyleSheet("border: 1px solid gray; border-radius: 5px;")
#         return super().eventFilter(obj, event)
