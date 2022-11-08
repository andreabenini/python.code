# PyAutoGUI lets Python scripts control the mouse and keyboard to automate interactions with other applications,
#   it works on Windows, macOS, and Linux, and runs on Python 2 and 3.
#       https://pyautogui.readthedocs.io/en/latest/

import pyautogui as pag

# Simple
pag.doubleClick(150, 150)
pag.write('Write some text here', interval=0.25)

# Mouse Dragging
distance = 200
while distance > 0:
    pyautogui.drag(distance, 0, duration=0.5)   # move right
    distance -= 5
    pyautogui.drag(0, distance, duration=0.5)   # move down
    pyautogui.drag(-distance, 0, duration=0.5)  # move left
    distance -= 5
    pyautogui.drag(0, -distance, duration=0.5)
