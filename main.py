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

# COLORS (check using main.py and looking at frame color values detected)
_,YELLOW = (81, 180, 198), (88, 180, 201)
GRAY = (126, 124, 120)
_,GREEN = (97, 170, 113), (100, 170, 106)
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
    print(f"Unknown color detected: {inp}")
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

def try_word(word):
    for letter in word:
        ClickKey(string_to_hex_match[letter])
    ClickKey(ENTER)
    
offsetTime = 2

def get_count(l, e, c=0):
    for x in l:
        if e == x:
            c += 1
    return c

def run(word_list, first=True, attempts=None):
    if first:
        attempts = []
    words = word_list[::]
    word = words[0]
    try_word(word)
    attempts += [[l for l in word]]
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
    frame = frame[int(image_shape[0]*0.2):int(image_shape[0]*0.77), image_shape[1]//3:image_shape[1]*2//3]

    # Check the board is being captured (adjust above cropping if not)
    # cv2.imshow("Capture", frame)
    # cv2.waitKey(0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2) # PERFECT THRESH
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Test the thresholding (shouldn't be needed)
    # cv2.imshow("Thresh", thresh)
    # cv2.waitKey(0)
    
    output = frame.copy()

    board = np.zeros((ROWS, LENGTH, 3))
    index = -1
    for contour in reversed(contours):
        (x,y,w,h) = cv2.boundingRect(contour)
        if withinRange(w, 90, 100) and withinRange(h, 90, 100):
            cv2.rectangle(output, (x,y), (x+w,y+h), (255, 0, 255), 2)
            index += 1
            coords = (index//LENGTH, index%LENGTH)
            text_declaration(output, ",".join(str(n) for n in coords), x, y+h//2)
            cv2.circle(output, (x+w//3,y+4*w//5), 2, (255,0,0), 2, cv2.FILLED)
            board[coords[0]][coords[1]] = frame[y+4*w//5][x+w//3] #color

    # Test the board is being processed correctly
    # (tweaking parameters should correct any errors, again shouldn't be needed)
    # cv2.imshow("Output", output)
    # cv2.waitKey(0)

    for y, row in enumerate(board[:len(attempts)]):
        for x, col in enumerate(row):
            status, new_el = get_status(col.tolist()), [attempts[y][x], x]
            # print("Status of ("+str(y)+","+str(x)+") is "+status)
            try:
                if new_el not in letter_statuses[status]:
                    letter_statuses[status] += [new_el]
            except Exception as e:
                if "send" in sys.argv:
                    send(word)
                print("I just sent you a word")
                return

    # for y, row in enumerate(board[:len(attempts)]):
    #     for x, col in enumerate(row):
    #         for letter in attempts[y][x]:
    #             contained_letters = list(map(lambda x: x[0], letter_statuses["present"]+letter_statuses["correct"]))
    #             if letter in contained_letters and letter in list(map(lambda x: x[0], letter_statuses["absent"])):
    #                 print(f"{letter} occurs {get_count(contained_letters, letter)} times") # Counter works
    words = list(filter(lambda word: filtering_func(word, letter_statuses), words))
    if word in words:
        words.remove(word)
    print(words)
    run(words, False, attempts)

first = True

if __name__ == "__main__":
    while True:
        if first or not "auto" in sys.argv:
            print("Press enter to start, space to exit")
            while True:
                if keyboard.is_pressed('enter'):
                    first = False
                    break
                elif keyboard.is_pressed('space'):
                    exit()
        run(get_all_words())
        if "auto" in sys.argv:
            sleep(2.5)
            click(520, 575)
            click(300, 300)
            sleep(1.5)

# FIXME: auto currently doesn't work because Wordle added new menu