#coding:utf-8
import RPi.GPIO as GPIO
import time, sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def led(open, ledPin = 23):
    """Set LED's status"""
    print 'led',open
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, open)

def flickerLED(times = 1, ledPin = 23):
    GPIO.setup(ledPin, GPIO.OUT)
    for i in range(times):
        GPIO.output(ledPin, True)
        time.sleep(0.1)
        GPIO.output(ledPin, False)
        time.sleep(0.1)

def rotateMotor(steps, clockwise=True):
    if clockwise:
        arr = [0,1,2,3]
    else:
        arr = [3,2,1,0]

    ports = [10,12,16,18]
    for p in ports:
        GPIO.setup(p, GPIO.OUT)
    for x in range(steps):
        for j in arr:
            time.sleep(0.003)
            for i in range(4):
                if i == j:
                    GPIO.output(ports[i], True)
                else:
                    GPIO.output(ports[i], False)
    for p in ports:
        GPIO.output(ports[i], False)

def openDoor(steps = 270):
    clockwise = True
    rotateMotor(steps, clockwise)
    led(True)

def closeDoor(steps = 270):
    led(False)
    clockwise = False
    rotateMotor(steps, clockwise)

def openThenClose(steps = 270):
    openDoor(steps)
    time.sleep(3)
    closeDoor(steps)

class Keypad():
    
    KEYPAD = [
    [1,2,3,"A"],
    [4,5,6,"B"],
    [7,8,9,"C"],
    ["*",0,"#","D"]
    ]
     
    ROW    = [7,8,11,13]
    COLUMN = [15,22,24,26]
     
    def __init__(self):
        self.rowNum = len(self.ROW)
        self.columnNum = len(self.COLUMN)
        self.litLED = False

    def getKey(self):

        # Set all columns as output low
        for j in range(self.columnNum):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(self.rowNum):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(self.rowNum):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > self.rowNum-1:
            self.exit()
            return
        # light led
        led(True)
        self.litLED = True

        # Convert columns to input
        for j in range(self.columnNum):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(self.columnNum):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > self.columnNum-1:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(self.rowNum):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(self.columnNum):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # close led
        if self.litLED:
            led(False)