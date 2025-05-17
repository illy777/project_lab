#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains a class for acquiring data from the serial port for this specific application.

import serial

class SerialPort:
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serialConnection = None

    def connect(self):
        try:
            self.serialConnection = serial.Serial(self.port, self.baudrate)
            self.serialConnection.write(bytes(1)) #handshake
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")

    def disconnect(self):
        if self.serialConnection and self.serialConnection.is_open:
            self.serialConnection.close()
            print("Disconnected from serial port.")

    def readData(self):
        """Read raw data string from serial until end marker is found."""
        dataStr = ""
        while not ('\\r\\n' in dataStr):
            dataByte = self.serialConnection.read(self.serialConnection.inWaiting())
            if len(dataByte) > 0:
                dataStr += str(dataByte).split("'")[1]
        return dataStr

    def acquireData(self):
        """Combined method for compatibility."""
        self.serialConnection.write(b'e') # request data
        return self.readData()
    
    def __del__(self):
        self.disconnect()

class FileHandler:

    def readFile(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines