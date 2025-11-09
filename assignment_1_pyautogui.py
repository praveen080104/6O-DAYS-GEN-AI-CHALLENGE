import pyautogui
import time

time.sleep(2)

# Open Run dialog
pyautogui.hotkey('win', 'r')
time.sleep(1)

# Open Chrome (full path)
pyautogui.typewrite('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"\n')
time.sleep(4)

# Search YouTube for the song
pyautogui.typewrite("https://www.youtube.com/results?search_query=perfect+ed+sheeran\n")
time.sleep(6)  # wait for YouTube to load

# CLICK the first video using the given coordinates
pyautogui.moveTo(679, 400, duration=0.5)  # smooth move
pyautogui.click()  # clicks the first video

time.sleep(3)
pyautogui.press('f')
print("✅ Clicked first video at (679, 400)")