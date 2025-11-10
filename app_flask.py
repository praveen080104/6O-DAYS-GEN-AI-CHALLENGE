from flask import Flask
import pyautogui
import time

app = Flask(__name__)

@app.route('/play')
def play_song():

    time.sleep(2)

    # Open Run dialog
    pyautogui.hotkey('win', 'r')
    time.sleep(1)

    # Open Chrome
    pyautogui.typewrite('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"\n')
    time.sleep(4)

    # Open YouTube search
    pyautogui.typewrite("https://www.youtube.com/results?search_query=perfect+ed+sheeran\n")
    time.sleep(6)

    # Click first video (you can change coordinates if needed)
    pyautogui.moveTo(679, 400, duration=0.5)
    pyautogui.click()

    time.sleep(3)
    pyautogui.press('f')  # Full screen

    return "✅ Playing 'Perfect - Ed Sheeran' on YouTube!"

if __name__ == "__main__":
    app.run(debug=True)
