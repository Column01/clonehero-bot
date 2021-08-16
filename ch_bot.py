import cv2
import numpy as np
import time
from PIL import Image

# GREEN NOTE: 07790a, (7, 121, 10)
# RED NOTE: 7c0407, (124, 4, 7)
# YELLOW NOTE: CFCD36, (207, 205, 54)
# BLUE NOTE: 51a5d4, (81, 165, 212)
# ORANGE NOTE: cd9a18, (205, 154, 24)
# STARPOWER NOTE: 40cac7 (64, 202, 199)
# OPEN NOTE: 77179f, (119, 23, 159)

# End value is FPS value
MAX_FRAME_TIME = 1000 // 60

TOLERANCE = 5

_notes = {
    "GREEN": (7, 121, 10),
    "RED": (124, 4, 7),
    "YELLOW": (207, 205, 54),
    "BLUE": (81, 165, 212),
    "ORANGE": (205, 154, 24),
    "OPEN": (119, 23, 159),
    "STARPOWER": (64, 202, 199)
}

MASKS = {"indexes": {}}

i = 0
for note, color in _notes.items():
    MASKS["indexes"][i] = note
    i += 1

    MASKS[note] = {}

    # Make a one pixel RGB image from the color
    img = Image.new("RGB", [1,1], color=color)
    # Convert it to HSV
    hsvImg = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2HSV)
    # Convert it to a PIL HSV image
    pilhsvImg = Image.fromarray(hsvImg, "HSV")
    # Get the pixel HSV values as a list
    pixel_values = list(pilhsvImg.getdata())

    h_lower = pixel_values[0][0] - (TOLERANCE / 2) if pixel_values[0][0] - (TOLERANCE / 2) > 0 else 0
    s_lower = pixel_values[0][1] - TOLERANCE if pixel_values[0][1] - TOLERANCE > 0 else 0
    v_lower = pixel_values[0][2] - TOLERANCE if pixel_values[0][2] - TOLERANCE > 0 else 0

    h_upper = pixel_values[0][0] + (TOLERANCE / 2) if pixel_values[0][0] + (TOLERANCE / 2) <= 179 else 179
    s_upper = pixel_values[0][1] + TOLERANCE if pixel_values[0][1] + TOLERANCE <= 255 else 255
    v_upper = pixel_values[0][2] + TOLERANCE if pixel_values[0][2] + TOLERANCE <= 255 else 255
    MASKS[note]["lower"] = (h_lower, s_lower, v_lower)
    MASKS[note]["upper"] = (h_upper, s_upper, v_upper)


def crop(image):
    """ See: https://stackoverflow.com/a/59208291/9873471 """
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    if y_nonzero.shape[0] == 0 or x_nonzero.shape[0] == 0:
        return None
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]


frame_times = []

camera = cv2.VideoCapture(0)

ret, frame = camera.read() if camera.isOpened() else False, False


note_file = open("notes.txt", "w+")

# Macro for fast file write
write_notes = note_file.write

if ret:
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cur_it = 0

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

        if cropped is None:
            continue
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

        # Split cropped image into 5 equal columns. See: https://stackoverflow.com/questions/56896878/split-image-into-arbitrary-number-of-boxes
        h, w = cropped.shape[:2]
        chunks = 5
        detected = []
        # Variable so we can process open notes properly
        has_detection = False
        for i in range(chunks):
            # The current chunk to process
            chunk = cropped[:, i * w // chunks: (i + 1) * w // chunks]

            # Create a color mask for the current note and check for detections
            cur_note = MASKS["indexes"].get(i)
            mask = cv2.inRange(chunk, MASKS[cur_note]["lower"], MASKS[cur_note]["upper"])
            cropped_mask_y, cropped_mask_x = np.nonzero(mask)
            # No detection.
            if cropped_mask_y.shape[0] == 0 or cropped_mask_x[0] == 0:
                # # Try SP mask:
                # sp_mask = cv2.inRange(chunk, MASKS["STARPOWER"]["lower"], MASKS["STARPOWER"]["upper"])
                # cropped_spmask_y, cropped_spmask_x = np.nonzero(sp_mask)
                # # No detection
                # if cropped_spmask_y.shape[0] == 0 or cropped_spmask_x[0] == 0:
                #     detected.append("[ ]")
                # # Starpower detection, save it.
                # else:
                #     has_detection = True
                #     detected.append(f"[SP_{cur_note}]")
                detected.append("[ ]")
            # We have a detection, save it
            else:
                has_detection = True
                detected.append(f"[{cur_note}]")
                
        # # No detections this tick, try detecting open notes
        if not has_detection:
            open_mask = cv2.inRange(cropped, MASKS["OPEN"]["lower"], MASKS["OPEN"]["upper"])
            cropped_mask_y, cropped_mask_x = np.nonzero(open_mask)
            # No detection
            if cropped_mask_y.shape[0] == 0 or cropped_mask_x[0] == 0:
                # # Try SP mask:
                # sp_mask = cv2.inRange(chunk, MASKS["STARPOWER"]["lower"], MASKS["STARPOWER"]["upper"])
                # cropped_spmask_y, cropped_spmask_x = np.nonzero(sp_mask)
                # # No detection
                # if cropped_spmask_y.shape[0] == 0 or cropped_spmask_x[0] == 0:
                #     detected.append("[ ]")
                # # Starpower detection, save it.
                # else:
                #     has_detection = True
                #     detected.append(f"[SP_OPEN]")
                detected.append("[ ]")
            # We have a detection, save it
            else:
                has_detection = True
                detected.append("[OPEN]")
                
        # Print the detected list every 30 iterations for debuging purposes
        if cur_it == 30:
            print(", ".join(detected))
            cur_it = 0
        else:
            cur_it += 1

        write_notes(", ".join(detected))
        write_notes("\n")

        # Calculate the used time and wait for whatever is left for a 60fps loop
        end = time.time()
        frame_time = int((end - start) * 1000)

        # If we took more than the time required for 60fps, only wait 1ms
        wait_time = MAX_FRAME_TIME - frame_time if MAX_FRAME_TIME - frame_time > 0 else 1

        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

camera.release()
note_file.close()
