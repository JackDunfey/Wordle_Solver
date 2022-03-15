import numpy as np
from PIL import ImageGrab
import cv2
from keylib import *
from time import sleep
import keyboard
from words import *
import sys
from send import send

font = cv2.FONT_HERSHEY_SIMPLEX

screen = np.array(ImageGrab.grab())

# COLORS
YELLOW = (97, 182, 201)
GRAY = (126, 124, 120)
GREEN = (105, 171, 91)
WHITE = (255, 255, 255)

COLORS = {
    "YELLOW": YELLOW, 
    "GRAY": GRAY,
    "GREEN": GREEN,
    "WHITE": WHITE
}

def color_compare(t1,t2):
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            return False
    return True
def color_name(inp):
    for name, color in COLORS.items():
        if color_compare(inp,color):
            return name
    return "Unknown"
def get_status(inp):
    return {
        "YELLOW": "present",
        "GREEN": "correct",
        "GRAY": "absent",
        "WHITE": "EMPTY",
        "Unknown": "Unknown"
    }[color_name(inp)]
options = ["present","correct","absent","EMPTY"]
def get_int_status(inp):
    for i in range(len(options)):
        if get_status(inp) == options[i]:
            return i+1

cell_size = (62, 62)
cell_spacing = 4 # 4 pixels between cells

attack = True

ROWS = 6
LENGTH = 5

def text_declaration(frame, text,x,y):
    cv2.putText(frame, text=text,
        org=(int(x), int(y)),
        fontFace=font,
        fontScale=0.7,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA)

curr_key = None
def set_key(key):
    global curr_key
    if curr_key:
        ReleaseKey(curr_key)
    curr_key = key
    PressKey(key)
def reset_key():
    global curr_key
    if curr_key:
        curr_key = ReleaseKey(curr_key)

def withinRange(number, min, max):
    return number >= min and number <= max

attempts = []
def try_word(word):
    global attempts
    for letter in word:
        ClickKey(string_to_hex_match[letter])
    ClickKey(ENTER)
    attempts += [[l for l in word]]
    
offsetTime = 2

def get_count(l, e, c=0):
    for x in l:
        if e == x:
            c += 1
    return c

word = "" # guess
def run():
    global letter_statuses
    global words
    global word
    if True:
        word = words[0]
        try:
            try_word(word)
        except:
            pass
            # exit(69420)
        sleep(offsetTime)
        letter_statuses = {
            "present": [],
            "absent": [],
            "correct": []
        }
        img = ImageGrab.grab(bbox=(0, 0, screen.shape[1], screen.shape[0]))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        image_shape = frame.shape # rows, cols, channels
        frame = frame[image_shape[0]//4:image_shape[0]*2//3, image_shape[1]//3:image_shape[1]*2//3]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2) # PERFECT THRESH
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        output = frame.copy()

        board = np.zeros((ROWS, LENGTH, 3))
        index = -1
        for contour in reversed(contours):
            (x,y,w,h) = cv2.boundingRect(contour)
            if withinRange(w, 60, 64) and withinRange(h, 60, 64): # 62 +- 2
                cv2.rectangle(output, (x,y), (x+w,y+h), (255, 0, 255), 2)
                index += 1
                coords = (index//LENGTH, index%LENGTH)
                text_declaration(output, ",".join(str(n) for n in coords), x, y+h//2)
                cv2.circle(output, (x+w//3,y+4*w//5), 2, (255,0,0), 2, cv2.FILLED)
                board[coords[0]][coords[1]] = frame[y+4*w//5][x+w//3] #color
        for y, row in enumerate(board[:len(attempts)]):
            for x, col in enumerate(row):
                status, new_el = get_status(col.tolist()), [attempts[y][x], x]
                try:
                    if new_el not in letter_statuses[status]:
                        letter_statuses[status] += [new_el]
                except:
                    send(word)
                    if len(sys.argv) > 0 and sys.argv[1]:
                        PressKey(CTRL)
                        ClickKey(W)
                        ReleaseKey(CTRL)
                    print("I just sent you a word")
                    exit(0)

        for y, row in enumerate(board[:len(attempts)]):
            for x, col in enumerate(row):
                for letter in attempts[y][x]:
                    contained_letters = list(map(lambda x: x[0], letter_statuses["present"]+letter_statuses["correct"]))
                    if letter in contained_letters and letter in list(map(lambda x: x[0], letter_statuses["absent"])):
                        print(f"{letter} occurs {get_count(contained_letters, letter)} times") # Counter works
        words = list(filter(lambda word: filtering_func(word, letter_statuses), words))
        if word in words:
            words.remove(word)
        print(words)
        run()

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('space') or len(sys.argv) > 0 and sys.argv[1] == "auto":
            if len(sys.argv) > 0 and sys.argv[1] == "auto":
                # click(1000,100)
                click(300,200)
            break
    run()