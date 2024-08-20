import cv2 as cv
from mediapipe import Image, ImageFormat
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerResult, HandLandmarkerOptions, RunningMode

from draw import draw_landmarks_on_image

model_path = "./hand_landmarker.task"

def handle_frame(result: HandLandmarkerResult, output_image: Image, timestap_ms: int): # type: ignore
    # draw_landmarks_on_image()
    print(output_image.numpy_view())
    
    
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_path),
    running_mode=RunningMode.IMAGE,
    # result_callback=handle_frame,
    num_hands=2
)
with HandLandmarker.create_from_options(options) as landmarker:
    capture = cv.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        timestamp = capture.get(cv.CAP_PROP_POS_MSEC)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)

        result = landmarker.detect(mp_image)

        bum = draw_landmarks_on_image(rgb, result)

        cv.imshow('digga', cv.cvtColor(bum, cv.COLOR_RGB2BGR))
        if cv.waitKey(1) == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()
