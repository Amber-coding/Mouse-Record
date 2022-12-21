import pyautogui
from pynput import mouse
import time
import csv

# how long write a record
frequency = 1000
fileName = "out.txt"

curPos = ""
flag = True


def on_move(x, y):
    global curPos, curPosdo, curPosx, curPosy, curPostim, curhour, curmin, cursec
    curPosdo = "move"
    curPosx = x
    curPosy = y
    curPostim = time.ctime()
    result = time.localtime()
    curhour = result.tm_hour
    curmin = result.tm_min
    cursec = result.tm_sec

    curPos = f"move, {x}, {y}, {time.ctime()}, {curhour}, {curmin}, {cursec}"


def on_click(x, y, button, pressed):
    if x <= 0 & y <= 0:
        print("end record")
        writecsv("end record", "end record", "end record",
                 "end record", "end record", "end record", "end record")
        global flag
        flag = False
        return False

    result = time.localtime()
    if pressed:
        writecsv("pressed", x, y, time.ctime(),
                 result.tm_hour, result.tm_min, result.tm_sec)
        print(f"pressed, {x}, {y}, {time.ctime()}")
    else:
        writecsv("released", x, y, time.ctime(),
                 result.tm_hour, result.tm_min, result.tm_sec)
        print(f"released, {x}, {y}, {time.ctime()}")


def on_scroll(x, y, dx, dy):
    global flag
    flag = True
    return True


def main():
    global fp
    fp = open('outputtest.csv', 'w', newline='')
    fieldnames = ['Doing', 'x-coordinate',
                  'y-coordinate', 'time', 'hour', 'min', 'sec']
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()

    print("start record")
    listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    listener.start()
    while(flag):
        time.sleep(frequency * 0.001)
        writecsv(curPosdo, curPosx, curPosy,
                 curPostim, curhour, curmin, cursec)
        print(curPos)


def writecsv(doing, x, y, tim, hour, min, sec):
    fieldnames = ['Doing', 'x-coordinate',
                  'y-coordinate', 'time', 'hour', 'min', 'sec']
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writerow({'Doing': doing, 'x-coordinate': x,
                     'y-coordinate': y, 'time': tim, 'hour': hour, 'min': min, 'sec': sec})


if __name__ == '__main__':
    main()
