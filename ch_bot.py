import cv2
import numpy as np
import time


# GREEN NOTE: 07790a, (7, 121, 10)
# RED NOTE: 7c0407, (124, 4, 7)
# YELLOW NOTE: 796300, (121, 99, 0)
# BLUE NOTE: 003476, (0, 52, 118)
# ORANGE NOTE: 773a00, (119, 58, 0)
# OPEN NOTE: 77179f, (119, 23, 159)

# End value is FPS value
MAX_FRAME_TIME = 1000 // 60

TOLERANCE = 5

_notes = {
    "GREEN": (7, 121, 10),
    "RED": (124, 4, 7),
    "YELLOW": (121, 99, 0),
    "BLUE": (0, 52, 118),
    "ORANGE": (119, 58, 0),
    "OPEN": (119, 23, 159),
}

MASKS = {}

for note, color in _notes.items():
    MASKS[note] = {}
    MASKS[note]["lower"] = (color[0] - TOLERANCE, color[1] - TOLERANCE, color[2] - TOLERANCE)
    MASKS[note]["upper"] = (color[0] + TOLERANCE, color[1] + TOLERANCE, color[2] + TOLERANCE)

print(MASKS)

def crop(image):
    """ See: https://stackoverflow.com/a/59208291/9873471 """
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    if y_nonzero.shape[0] == 0 or x_nonzero.shape[0] == 0:
        return image
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]


frame_times = []

camera = cv2.VideoCapture(0)

ret, frame = camera.read() if camera.isOpened() else False, False 

if ret:
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        # Current time in MS
        start = time.time()
        # Capture the video frame
        ret, frame = camera.read()

        # Crop black outline off of frame
        try:
            cropped = crop(frame)
        except ValueError:
            print("VALUE ERROR!")
            continue
        # cv2.imshow("Cropped", cropped)

        # Split cropped image into 5 equal columns. See: https://stackoverflow.com/questions/56896878/split-image-into-arbitrary-number-of-boxes
        h, w = cropped.shape[:2]
        chunks = 5
        for i in range(chunks):
            chunk = cropped[:, i * w // chunks: (i + 1) * w // chunks]
            cv2.imshow(f"box{i}", chunk)

        end = time.time()
        frame_time = int((end - start) * 1000)
        wait_time = MAX_FRAME_TIME - frame_time if MAX_FRAME_TIME - frame_time > 0 else 1

        # frame_times.append(frame_time)

        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

# print(f"Raw frame times: {frame_times}")
# print(f"Average frame time: {sum(frame_times) / len(frame_times)}")
for i in range(5):
    cv2.destroyWindow(f"box{i}")
camera.release()
