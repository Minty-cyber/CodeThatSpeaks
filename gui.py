from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QStackedWidget
from PySide6.QtCore import Qt, QTimer, QEvent, QObject, Signal, QSize
from PySide6.QtGui import QCursor,  QIcon
from functools import partial

class ModernPage(QWidget):
    back_to_main = Signal()  

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top_row_layout = QHBoxLayout()
        layout.addLayout(top_row_layout)
        
        back_button = QPushButton(self)
        back_button.setIcon(QIcon("back-button.png")) 
        back_button.setStyleSheet("background-color: #333; border: none; color: whitesmoke;")  
        back_button.setFixedSize(50, 50)
        back_button.clicked.connect(self.go_to_main_window)
        top_row_layout.addWidget(back_button)
        
        main_title_label = QLabel("BasicLingua", self)
        main_title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: whitesmoke;")
        main_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row_layout.addWidget(main_title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.addSpacing(50)
        
        title_label = QLabel("Text Translation", self)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px; color: whitesmoke;")
        input_layout.addWidget(title_label)

        
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("User Input")
        self.user_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.user_input.setFixedSize(300, 40)
        input_layout.addWidget(self.user_input)

        self.target_language_input = QLineEdit(self)
        self.target_language_input.setPlaceholderText("Target Language")
        self.target_language_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: whitesmoke; font-size: 15px; text-align: center;")
        self.target_language_input.setFixedSize(300, 40)
        input_layout.addWidget(self.target_language_input)

        layout.addLayout(input_layout)
        
        button_layout = QHBoxLayout()
        input_layout.addLayout(button_layout)

        translate_button = QPushButton("Translate", self)
        translate_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        translate_button.setFixedSize(100, 50)
        button_layout.addWidget(translate_button)
        
        refresh_button = QPushButton("Refresh", self)
        refresh_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        refresh_button.setFixedSize(100, 50)
        button_layout.addWidget(refresh_button)
        
        
    def go_to_main_window(self):
        self.back_to_main.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Button Cluster")
        self.setStyleSheet("background-color: #333;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_main_window()
        self.setup_modern_page()

    def setup_main_window(self):
        main_window_widget = QWidget()
        layout = QGridLayout(main_window_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        

        button_texts = ["Text-Translation", "Button 1", "Button 2", "Button 3", "Button 4", "Button 5",
                        "Extract Patterns", "2", '3', '4', '5', '6', "8", '9', '10']
        rows = 4
        cols = 6
        for i, text in enumerate(button_texts):
            button = QPushButton(text, self)
            button.setStyleSheet(
                "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
            button.setFixedSize(button.sizeHint())
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(self.show_modern_page)
            row = i // cols
            col = i % cols
            layout.addWidget(button, row, col)

        self.central_widget.addWidget(main_window_widget)

    def setup_modern_page(self):
        modern_page = ModernPage()
        modern_page.back_to_main.connect(self.show_main_window)
        self.central_widget.addWidget(modern_page)

    def show_modern_page(self):
        self.central_widget.setCurrentIndex(1)

    def show_main_window(self):
        self.central_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
