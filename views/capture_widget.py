import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from mediapipe import Image, ImageFormat
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, HandLandmarkerResult, RunningMode

from draw import draw_landmarks_on_image


class CaptureThread(QThread):
    updateLandmarks = Signal(HandLandmarkerResult)
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self._status = True
        self._model_path =  "./hand_landmarker.task"


    def run(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(self._model_path),
            running_mode=RunningMode.IMAGE,
            num_hands=2
        )
        with HandLandmarker.create_from_options(options) as landmarker:
            cap = cv2.VideoCapture(0)
            while self._status:
                ret, frame = cap.read()
                if not ret:
                    continue

                color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                mp_image = Image(image_format=ImageFormat.SRGB, data=color)

                result = landmarker.detect(mp_image)
                self.updateLandmarks.emit(result)

                color_with_landmarks = draw_landmarks_on_image(color, result)

                height, width, _ = color_with_landmarks.shape

                img = QImage(color_with_landmarks.data, width, height, QImage.Format.Format_RGB888)

                self.updateFrame.emit(img)
            cap.release()

    def quit(self) -> None:
        self._status = False
        return super().quit()
