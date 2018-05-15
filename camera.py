import io
import time
import picamera
import cv2
import numpy as np
import datetime
import BlynkLib
import logging
import random
from PIL import Image
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit
import os
os.chdir ("/home/pi/viral-load/photos")

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()
cellNumber = 0

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(1000, 1)  # max steps/rev, motor port #1
myStepper.setSpeed(1000)# max RPM

def moveMotorForwardSlow():
    myStepper.step(1825, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.INTERLEAVE)
    #takePic()

def moveMotorForwardFast():
    myStepper.step(400, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
    #takePic()
    
def moveMotorBackwardSlow():
    myStepper.step(1825, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.INTERLEAVE)
    #takePic()

def moveMotorBackwardFast():
    myStepper.step(400, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)
    #takePic()

def takePic():
    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
    # Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)

    file = datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg")
    cv2.imwrite(file, image)

    I = Image.open(file); W, H = I.size; A = W * H
    D = [sum(c) for c in I.getdata()]
    Bh = [0] * H; Ch = [0] * H
    Bv = [0] * W; Cv = [0] * W

    # Flood-fill
    Background = 3 * 255 + 1; S = [0]
    while S:
        i = S.pop(); c = D[i]
        if c != Background:
            D[i] = Background
            
            Bh[int(i / W)] += c; Ch[int(i / W)] += 1
            Bv[int(i % W)] += c; Cv[int(i % W)] += 1
            S += [(i + o) % A for o in [1, -1, W, -W] if abs(D[(i + o) % A] - c) < 10]

    # Eliminate "trapped" areas
    for i in range(H): Bh[i] /= float(max(Ch[i], 1))
    for i in range(W): Bv[i] /= float(max(Cv[i], 1))
    for i in range(A):
        a = (Bh[int(i / W)] + Bv[int(i % W)]) / 2
        if D[i] >= a: D[i] = Background

    # Estimate grain count
    Foreground = -1; avg_grain_area = 80; grain_count = 0
    for i in range(A):
        if Foreground < D[i] < Background:
            S = [i]; area = 0
            while S:
                j = S.pop() % A
                if Foreground < D[j] < Background:
                    D[j] = Foreground; area += 1
                    S += [j - 1, j + 1, j - W, j + W]
            grain_count += int(round(area / avg_grain_area))
    cellNumber = grain_count
    print('Cell Number: ', cellNumber)

def printCellCount(): 
    return cellNumber

blynk = BlynkLib.Blynk('be1080f0d64243aba202cb9046a22b4e')

# Register virtual pin handler
@blynk.VIRTUAL_READ(2)
def v2_read_handler():
    # This widget will show some time in seconds..
    blynk.virtual_write(2, time.ticks_ms() // 1000)

# Register virtual pin handler
@blynk.VIRTUAL_WRITE(4)
def v4_write_handler(value):
    if value:
        blynk.virtual_write(4, takePic())

@blynk.VIRTUAL_WRITE(6)
def v6_write_handler(value):
    if value:
        blynk.virtual_write(6, moveMotorForwardSlow())

@blynk.VIRTUAL_WRITE(8)
def v8_write_handler(value):
    if value:
        blynk.virtual_write(8, moveMotorBackwardSlow())

@blynk.VIRTUAL_READ(10)
def v10_read_handler():
    # This widget will show some time in seconds..
    blynk.virtual_write(10, printCellCount())

@blynk.VIRTUAL_WRITE(12)
def v12_write_handler(value):
    if value:
        blynk.virtual_write(12, moveMotorForwardFast())

@blynk.VIRTUAL_WRITE(14)
def v14_write_handler(value):
    if value:
        blynk.virtual_write(14, moveMotorBackwardFast())
    
blynk.run()




