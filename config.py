"""
Configuration file for configuring the bot
"""

# Default values I was able to get working for colors, these tend to be worse than detecting the tops of the notes as is set below.
# GREEN NOTE: 07790a, (7, 121, 10)
# RED NOTE: 7c0407, (124, 4, 7)
# YELLOW NOTE: CFCD36, (207, 205, 54)
# BLUE NOTE: 51a5d4, (81, 165, 212)
# ORANGE NOTE: cd9a18, (205, 154, 24)
# STARPOWER NOTE: 40cac7 (64, 202, 199)
# OPEN NOTE: 6e1191, (110, 17, 145)

# Plus or Minus to the below color values as a detection tolerance.
TOLERANCE = 10

# RGB Values for the tops of the notes, used for detection along with the above tolerance value
NOTES = {
    "GREEN": (220, 228, 228),
    "RED": (220, 228, 228),
    "YELLOW": (220, 228, 228),
    "BLUE": (220, 228, 228),
    "ORANGE": (220, 228, 228),
    "OPEN": (110, 17, 145),
    "STARPOWER": (85, 249, 245)
}

# Sets the FPS value (end number) Default: 60
MAX_FRAME_TIME = 1000 // 60

# Shows the cropped output that the bot sees in a new window
SHOW_OUTPUT = False

# Number of frames to wait before strumming. Default: 1
FRAMES_TILL_STRUM = 1

# Whether to save detected notes and print them out every so often. Default: False
SAVE_NOTES = False

# Whether to write detections to a text file. Default: False
SAVE_NOTES_TO_FILE = True

# Keybindings to use for playing a note
NOTE_MAPPING = {
    "GREEN": "~",
    "RED": "1",
    "YELLOW": "2",
    "BLUE": "3",
    "ORANGE": "4"
}

# Key binding for strumming
STRUM = "up"

### DO NOT TOUCH BELOW THIS LINE ###

WAIT_FOR_STRUM = (MAX_FRAME_TIME * FRAMES_TILL_STRUM) / 1000

MASKS = {"indexes": {}}

i = 0
for note, color in NOTES.items():
    MASKS["indexes"][i] = note
    i += 1

    MASKS[note] = {}

    # RGB to BGR conversion... thanks CV2... not.
    pixel_values = color[::-1]

    h_lower = pixel_values[0] - TOLERANCE if pixel_values[0] - TOLERANCE > 0 else 0
    s_lower = pixel_values[1] - TOLERANCE if pixel_values[1] - TOLERANCE > 0 else 0
    v_lower = pixel_values[2] - TOLERANCE if pixel_values[2] - TOLERANCE > 0 else 0

    h_upper = pixel_values[0] + TOLERANCE if pixel_values[0] + TOLERANCE <= 255 else 255
    s_upper = pixel_values[1] + TOLERANCE if pixel_values[1] + TOLERANCE <= 255 else 255
    v_upper = pixel_values[2] + TOLERANCE if pixel_values[2] + TOLERANCE <= 255 else 255
    MASKS[note]["lower"] = (h_lower, s_lower, v_lower)
    MASKS[note]["upper"] = (h_upper, s_upper, v_upper)
