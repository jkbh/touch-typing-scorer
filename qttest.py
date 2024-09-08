import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow
from PySide6.QtUiTools import QUiLoader
                                                     
class Menu(QVBoxLayout):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        startButton = QPushButton("Start")
        calibrateButton = QPushButton("Calibrate")

        self.addWidget(startButton)
        self.addWidget(calibrateButton)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    menu = Menu(window)
    window.show()
    sys.exit(app.exec())