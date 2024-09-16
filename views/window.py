from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel

from views.capture_widget import CaptureThread


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Patterns detection")
        self.setGeometry(0, 0, 1280, 720)

        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")

        exit = QAction("Exit", self, triggered=QApplication.instance().quit)
        self.menu_file.addAction(exit)

        # Create a label for the display camera
        self.label = QLabel(self)
        self.label.setFixedSize(1280, 720)

        # Thread in charge of updating the image
        self.th = CaptureThread(self)
        self.th.updateFrame.connect(self.setImage)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.th.start()

    def closeEvent(self, event) -> None:
        self.th.quit()
        print("closing webcam thread...")
        self.th.wait()
        return super().closeEvent(event)

    @Slot(QImage)
    def setImage(self, image: QImage):
        scaled = image.scaled(1280, 720)
        self.label.setPixmap(QPixmap.fromImage(scaled))
