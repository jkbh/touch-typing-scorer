import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage


class CaptureThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self._status = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.status:
            ret, frame = cap.read()
            if not ret:
                continue

            # detect, draw ...

            color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, _ = color.shape

            img = QImage(color.data, width, height, QImage.Format.Format_RGB888)

            self.updateFrame.emit(img)
        cap.release()

    def quit(self) -> None:
        self.status = False
        return super().quit()
