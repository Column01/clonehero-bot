import time

import cv2
import numpy as np
import keyboard
# from PIL import Image

from config import *

def crop(image):
    """ See: https://stackoverflow.com/a/59208291/9873471 """
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    if y_nonzero.shape[0] == 0 or x_nonzero.shape[0] == 0:
        return None
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

frame_times = []

camera = cv2.VideoCapture(0)

ret, frame = camera.read() if camera.isOpened() else False, False

if SAVE_NOTES_TO_FILE:
    note_file = open("notes.txt", "w+")

    # Macro for fast file write
    write_notes = note_file.write

# Macro for send key
press_key = keyboard.press
# Macro for release key
release_key = keyboard.release
# Macro for press and release
press_and_release = keyboard.press_and_release
# Macro for is_pressed
is_pressed = keyboard.is_pressed

if ret:
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cur_it = 0
    last_strum = 0

    while True:
        to_press = []
        to_depress = []
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
        if SAVE_NOTES or SAVE_NOTES_TO_FILE:
            detected = []
        # Variable so we can process open notes properly
        has_detection = False
        for i in range(chunks):
            # The current chunk to process
            chunk = cropped[:, i * w // chunks: (i + 1) * w // chunks]

            # Create a color mask for the current note and check for detections
            cur_note = MASKS["indexes"].get(i)
            # Get the key for the current note
            key = NOTE_MAPPING.get(cur_note)

            mask = cv2.inRange(chunk, MASKS[cur_note]["lower"], MASKS[cur_note]["upper"])
            cropped_mask_y, cropped_mask_x = np.nonzero(mask)

            # No detection.
            if cropped_mask_y.shape[0] == 0 or cropped_mask_x[0] == 0:
                # Try SP mask:
                sp_mask = cv2.inRange(chunk, MASKS["STARPOWER"]["lower"], MASKS["STARPOWER"]["upper"])
                cropped_spmask_y, cropped_spmask_x = np.nonzero(sp_mask)
                # No detection
                if cropped_spmask_y.shape[0] == 0 or cropped_spmask_x[0] == 0:
                    if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append("[ ]")

                    to_depress.append(key)
                # Starpower detection, save it.
                else:
                    has_detection = True
                    if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append(f"[SP_{cur_note}]")

                    # Press the key if its not pressed
                    to_press.append(key)
            # We have a detection, save it
            else:
                has_detection = True
                if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append(f"[{cur_note}]")
            
                # Press the key if its not pressed
                to_press.append(key)

        # No detections this tick, try detecting open notes
        if not has_detection:
            open_mask = cv2.inRange(cropped, MASKS["OPEN"]["lower"], MASKS["OPEN"]["upper"])
            cropped_mask_y, cropped_mask_x = np.nonzero(open_mask)
            # No detection
            if cropped_mask_y.shape[0] == 0 or cropped_mask_x[0] == 0:
                # Try SP mask:
                sp_mask = cv2.inRange(chunk, MASKS["STARPOWER"]["lower"], MASKS["STARPOWER"]["upper"])
                cropped_spmask_y, cropped_spmask_x = np.nonzero(sp_mask)
                # No detection
                if cropped_spmask_y.shape[0] == 0 or cropped_spmask_x[0] == 0:
                    if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append("[ ]")
                # Starpower detection, save it.
                else:
                    has_detection = True
                    if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append(f"[SP_OPEN]")

            # We have a detection, save it.
            else:
                has_detection = True
                if SAVE_NOTES or SAVE_NOTES_TO_FILE: detected.append("[OPEN]")

        # We have a detection, all keys should be pressed/release and then we can strum.
        if has_detection:
            for key in to_depress:
                release_key(key)
            for key in to_press:
                press_key(key)
            time.sleep((MAX_FRAME_TIME * FRAMES_TILL_STRUM) / 1000)
            press_and_release(STRUM)

        if SAVE_NOTES:
            # Print the detected list every 30 iterations for debuging purposes
            if cur_it == 30:
                print(", ".join(detected))
                cur_it = 0
            else:
                cur_it += 1

        if SAVE_NOTES_TO_FILE:
            write_notes(", ".join(detected))
            write_notes("\n")

        # Calculate the used time and wait for whatever is left for a 60fps loop
        end = time.time()
        frame_time = int((end - start) * 1000)

        # If we took more than the time required for 60fps, only wait 1ms
        wait_time = MAX_FRAME_TIME - frame_time
        if wait_time < 0: wait_time = 1

        # Wait for calculated frame time delay
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

camera.release()

if SAVE_NOTES_TO_FILE:
    note_file.close()
