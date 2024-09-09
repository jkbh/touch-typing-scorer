import sys
import cv2
import time
from PySide6.QtCore import QThread, Signal, Qt, Slot
from PySide6.QtGui import QImage, QPixmap, QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QLabel

class CaptureThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.cap = True
        self.status = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # detect, draw ...

            color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, channels = color.shape
            
            img = QImage(color.data, width, height, QImage.Format_RGB888)
            
            self.updateFrame.emit(img)
        sys.exit(-1)

if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())