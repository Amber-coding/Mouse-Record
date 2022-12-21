import pyautogui
from pynput import mouse
import time
import csv
import serial
import time
import threading

# how long write a record
frequency = 1000
fileName = "out.txt"

curPos = ""
flag = True

Connected = True
PulseWidth = 0.01


def ReadThread(port):
    while Connected:
        if port.inWaiting() > 0:
            print("0x%X" % ord(port.read(1)))


'''
# in "Ports /COM & LPT)" and enter the COM port number in the constructor.
port = serial.Serial("COM6")
# Start the read thread
thread = threading.Thread(target=ReadThread, args=(port,))
thread.start()
# Set the port to an initial state
port.write([0x00])
time.sleep(PulseWidth)
'''


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

        # Reset the port to its default state
        port.write([0xFF])
        time.sleep(PulseWidth)
        # Terminate the read thread
        Connected = False
        thread.join(1.0)
        # Close the serial port
        port.close()

        return False

    result = time.localtime()
    if pressed:

        writecsv("pressed", x, y, time.ctime(),
                 result.tm_hour, result.tm_min, result.tm_sec)
        print(f"pressed, {x}, {y}, {time.ctime()}")

        # Set Bit 0, Pin 2 of the Output(to Amp) connector
        port.write([0x01])
        time.sleep(PulseWidth)

    else:
        # Reset Bit 0, Pin 2 of the Output(to Amp) connector
        port.write([0x00])
        time.sleep(PulseWidth)

        writecsv("released", x, y, time.ctime(),
                 result.tm_hour, result.tm_min, result.tm_sec)
        print(f"released, {x}, {y}, {time.ctime()}")


def on_scroll(x, y, dx, dy):
    global flag
    flag = True
    return True


def main():

    # in "Ports /COM & LPT)" and enter the COM port number in the constructor.
    global port
    port = serial.Serial("COM3")
    # Start the read thread
    global thread
    thread = threading.Thread(target=ReadThread, args=(port,))
    thread.start()
    # Set the port to an initial state
    port.write([0x00])
    time.sleep(PulseWidth)

    global fp
    fp = open('output.csv', 'w', newline='')
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
    # print("1")
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
