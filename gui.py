from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QStackedWidget, QProgressBar, QSizePolicy, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QIcon, QCursor, QTextOption
from functools import partial
from basiclingua import BasicLingua
import threading
from docx import Document

class TextTranslationPage(QWidget):
    back_to_main = Signal()
    translation_completed = Signal(str)
    translation_error = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_row_layout = QHBoxLayout()
        layout.addLayout(top_row_layout)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("back-button.png"))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                color: white;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #45a049; /* Change color on hover */
            }
        """)
        back_button.setFixedSize(70, 100)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.clicked.connect(self.go_to_main_window)
        top_row_layout.addWidget(back_button)

        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_fields_layout = QVBoxLayout()
        input_fields_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.api_input = QLineEdit(self)
        self.api_input.setPlaceholderText("Enter API Key")
        self.api_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: black; font-size: 15px; text-align: center;")
        self.api_input.setFixedSize(300, 40)
        self.api_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.api_input.installEventFilter(self)
        input_fields_layout.addWidget(self.api_input)

        self.user_input = QTextEdit(self) 
        self.user_input.setPlaceholderText("User Input")
        self.user_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: black; font-size: 15px; text-align: center;")
        self.user_input.setFixedSize(300, 100) 
        self.user_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.user_input.installEventFilter(self)
        
        input_fields_layout.addWidget(self.user_input)
        
        self.target_language_input = QLineEdit(self)
        self.target_language_input.setPlaceholderText("Target Language")
        self.target_language_input.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: black; font-size: 15px; text-align: center;")
        self.target_language_input.setFixedSize(300, 40)
        self.target_language_input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.target_language_input.installEventFilter(self)
        input_fields_layout.addWidget(self.target_language_input)

        input_layout.addLayout(input_fields_layout)
        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addLayout(button_layout)

        translate_button = QPushButton("Translate", self)
        translate_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        translate_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        translate_button.setFixedSize(100, 50)
        translate_button.clicked.connect(self.translate_text)
        button_layout.addWidget(translate_button)

        self.loader = QProgressBar(self)
        self.loader.setStyleSheet("QProgressBar {"
                                  "border: 2px solid grey;"
                                  "border-radius: 5px;"
                                  "text-align: center;"
                                  "background-color: #333;"
                                  "}"
                                  "QProgressBar::chunk {"
                                  "background-color: #4CAF50;"
                                  "}")
        self.loader.setMinimum(0)
        self.loader.setMaximum(0)
        self.loader.setValue(0)
        self.loader.setFixedSize(100, 50)
        self.loader.hide()
        button_layout.addWidget(self.loader)

        self.result_text_edit = QTextEdit(self)
        self.result_text_edit.setStyleSheet("font-size: 18px; color: whitesmoke; background-color: #444; border: 1px solid #555; border-radius: 10px;")

        self.result_text_edit.setReadOnly(True)
        self.result_text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.result_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_layout.addWidget(self.result_text_edit)

        refresh_button = QPushButton("Refresh", self)
        refresh_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        refresh_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_button.setFixedSize(100, 50)
        refresh_button.clicked.connect(self.refresh_fields)
        button_layout.addWidget(refresh_button)

        self.download_button = QPushButton("Download Word", self)
        self.download_button.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px; border: none; border-radius: 5px;")
        self.download_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button.setFixedSize(150, 50)
        self.download_button.clicked.connect(self.download_word)
        button_layout.addWidget(self.download_button)

    def go_to_main_window(self):
        self.back_to_main.emit()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            obj.setStyleSheet("border: 2px solid #160202; border-radius: 5px; color: black; font-size: 15px;")
        elif event.type() == QEvent.FocusOut:
            obj.setStyleSheet("border: 1px solid gray; border-radius: 5px; color: black; font-size: 15px;")
        return super().eventFilter(obj, event)

    def translate_text(self):
        api_key = self.api_input.text()
        user_input = self.user_input.toPlainText()
        target_lang = self.target_language_input.text()

        translation_thread = threading.Thread(target=self.perform_translation, args=(api_key, user_input, target_lang))
        translation_thread.start()

    def perform_translation(self, api_key, user_input, target_lang):
        try:
            self.loader.show()
            client = BasicLingua(api_key)
            translated_text = client.text_translate(user_input, target_lang)
            self.translation_completed.emit(translated_text)
        except ValueError as e:
            self.translation_error.emit(str(e))
        finally:
            self.loader.hide()

    def refresh_fields(self):
        self.api_input.clear()
        self.user_input.clear()
        self.target_language_input.clear()
        self.result_text_edit.clear()

    def download_word(self):
        translated_text = self.result_text_edit.toPlainText()
        if translated_text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Word", "", "Word Files (*.docx)")
            if file_path:
                self.generate_word(translated_text, file_path)
                QMessageBox.information(self, "Download", f"Word document saved as {file_path}.")
        else:
            QMessageBox.warning(self, "No Translated Text", "Please perform translation before downloading Word document.")

    def generate_word(self, translated_text, file_path):
        doc = Document()
        doc.add_paragraph(translated_text)
        doc.save(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Button Cluster")
        self.setStyleSheet("background-color: #fff;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_main_window()
        self.setup_text_translation_page()

        self.setFixedSize(70, 70)

    def setup_main_window(self):
        main_window_widget = QWidget()
        layout = QVBoxLayout(main_window_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        main_title_label = QLabel("Text Translator", self)
        main_title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: black;")
        layout.addWidget(main_title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(60)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        button_1 = QPushButton("Text Translation", self)
        button_1.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 20px; padding: 10px; border: none; border-radius: 10px;")
        button_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button_1.clicked.connect(self.show_text_translation_page)
        grid_layout.addWidget(button_1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.central_widget.addWidget(main_window_widget)

    def setup_text_translation_page(self):
        text_translation_page = TextTranslationPage()
        text_translation_page.back_to_main.connect(self.show_main_window)
        text_translation_page.translation_completed.connect(self.display_translated_text)
        text_translation_page.translation_error.connect(self.display_translation_error)
        self.central_widget.addWidget(text_translation_page)

    def show_text_translation_page(self):
        self.central_widget.setCurrentIndex(1)

    def show_main_window(self):
        self.central_widget.setCurrentIndex(0)

    def display_translated_text(self, translated_text):
        current_widget = self.central_widget.currentWidget()
        if isinstance(current_widget, TextTranslationPage):
            current_widget.result_text_edit.setText(translated_text)

    def display_translation_error(self, error_message):
        current_widget = self.central_widget.currentWidget()
        if isinstance(current_widget, TextTranslationPage):
            current_widget.result_text_edit.setText(f"Translation Error: {error_message}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
