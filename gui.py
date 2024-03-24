import sys
import pyttsx3
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import Qt, QTimer, Signal
from functools import partial
from auto import *

class ModernPage(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout(self)
        
        label = QLabel("Modern Page", self)
        label.setStyleSheet("font-size: 24px; color: black;")
        layout.addWidget(label)

        text_edit = QTextEdit(text, self)
        text_edit.setStyleSheet("background-color: #E9F1FA; color: black; border: 2px solid #4CAF50; border-radius: 10px;")
        layout.addWidget(text_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    window_opened = Signal()  

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Button Cluster")
        self.setFixedSize(800, 600)  
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        
        self.setStyleSheet("background-color: #E9F1FA;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout(self.central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_texts = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5"]
        row = 0
        col = 0
        for text in button_texts:
            button = QPushButton(text, self)
            button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 10px; padding: 10px; border: none; border-radius: 38px;")
            button.setFixedSize(100, 50) 
            button.clicked.connect(partial(self.showModernPage, text))
            layout.addWidget(button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1
        
        self.window_opened.connect(speak_with_window_open)  

        QTimer.singleShot(1000, self.window_opened.emit)  
    
    def showModernPage(self, text):
        self.modern_page = ModernPage(text)
        self.setCentralWidget(self.modern_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
