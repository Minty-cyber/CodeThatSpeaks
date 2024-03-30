import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Create horizontal layout for the first two inputs
        horizontal_layout = QHBoxLayout()

        # First input
        input1 = QLineEdit()
        horizontal_layout.addWidget(input1)

        # Add horizontal layout to the main vertical layout
        main_layout.addLayout(horizontal_layout)

        # Second input
        input2 = QLineEdit()
        main_layout.addWidget(input2)
        
        # Third input aligned horizontally with the first two inputs
        input3 = QLineEdit()
        input3.setFixedHeight(60)  # Set a larger height for the third input
        main_layout.addWidget(input3)

        # Set the main layout for the widget
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
