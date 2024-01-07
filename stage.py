import math
import serial
import time
from numpy import sign
from enum import Enum, auto
from gpiozero import Button

class Methods(Enum):
    step_size = auto()
    frequency = auto()


def distance(p1, p2) -> float:
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


class Serial:
    def __init__(self):
        self.open_com()

    def open_com(self):
        while True:
            for i in range(10):
                try:
                    self.ser = serial.Serial(port=f'dev/ttyUSB0', baudrate=9600)
                    if self.ser.is_open:
                        print(f'connection on COM{i}.')
                    else:
                        input('unexpected error')
                    return  # success!
                except serial.serialutil.SerialException as e:  # error while opening com
                    # print(e.__repr__())
                    continue
            time.sleep(2)

        raise Exception('Could not open a serial port')

    def read_until(self, conditional_byte, exclude_conditional_byte=True):
        content = bytearray()
        byte = None
        while byte != conditional_byte:
            if self.ser.in_waiting:
                byte = self.ser.read(1)
                # exclude conditional
                if exclude_conditional_byte:
                    if byte == conditional_byte:
                        return content
                # append byte
                content += byte
        return content

    def read(self):
        START_BYTE = b'\x02'
        END_BYTE = b'\x03'

        # wait for start byte
        self.read_until(START_BYTE)

        # read until end byte
        response = self.read_until(END_BYTE)
        return response

    def readline(self):
        line = self.ser.readline()
        return line

    def send(self, msg) -> None:
        written = self.ser.write((chr(2) + '0' + msg + chr(3)).encode('ascii'))
        response = self.read()
        return response

if __name__ == '__main__':
    s = Serial()
    s.send('XS')

    # set the status of the motor
    rotating = False

    while True:
        button.wait_for_press()
        if rotating:
            s.send('XS')
            rotating = False
        elif not rotating:
            s.send('XL+')
            rotating = True


