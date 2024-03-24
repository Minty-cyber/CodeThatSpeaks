import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, QTimer, QEvent, QObject, Signal
from PySide6.QtGui import QCursor 
from functools import partial
from voice import *

class ModernPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout()) 
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.layout().setContentsMargins(0, -200, 0, 0)

        self.title_label = QLabel("Text Translation", self)
        self.title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px; color: whitesmoke;")
        self.layout().addWidget(self.title_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("User Input")
        self.username_input.setStyleSheet("border: 1px solid gray; border-radius: 5px;")
        self.username_input.setFixedSize(300, 40)  
        self.layout().addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Target Language")
        self.password_input.setFixedSize(300, 40) 
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout().addWidget(self.password_input)

        self.translate_button = QPushButton("Translate", self)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        self.login_button.setFixedSize(100, 50) 
        self.layout().addWidget(self.login_button)

        
        self.username_input.installEventFilter(self)
        self.password_input.installEventFilter(self)

    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            obj.setStyleSheet("border: 2px solid #160202; border-radius: 5px;")
        elif event.type() == QEvent.FocusOut:
            obj.setStyleSheet("border: 1px solid gray; border-radius: 5px;")
        return super().eventFilter(obj, event)


class MainWindow(QMainWindow):
    window_opened = Signal()  

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Button Cluster")
        self.setFixedSize(800, 600)  
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        
        self.setStyleSheet("background-color: #333;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout(self.central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_texts = ["Text-Translation", "Button 1", "Button 2", 
                        "Button 3", "Button 4", "Button 5", 
                        "Extract Patterns", "2", '3']
        row = 0
        col = 0
        for text in button_texts:
            button = QPushButton(text, self)
            button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
            button.setFixedSize(button.sizeHint())
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  
            button.clicked.connect(partial(self.showModernPage, text))
            layout.addWidget(button, row, col)
            col += 1
            if col == 6:
                col = 0
                row += 1
        
        self.window_opened.connect(speak_with_window_open)    

        QTimer.singleShot(1000, self.window_opened.emit)  
    
    
    
    def showModernPage(self, text):
        self.modern_page = ModernPage()
        self.setCentralWidget(self.modern_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
