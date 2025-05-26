# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
#
# Descritpion: This module contains a class for acquiring data from the serial port for this specific application.

import serial
import numpy as np
from app.app import DataAcquirer

class SerialPort(DataAcquirer):
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

    def _read_data(self):
        """Read raw data string from serial until end marker is found."""
        dataStr = ""
        while not ('\\r\\n' in dataStr):
            dataByte = self.serialConnection.read(self.serialConnection.inWaiting())
            if len(dataByte) > 0:
                dataStr += str(dataByte).split("'")[1]
        return dataStr

    def acquire_data(self) -> np.ndarray:
        data = self._read_data()
        return self._parse_data(data)
        
    def _parse_data(self, source: str) -> np.ndarray:
        """Process the raw data string into a list of floats."""
        data_str = source.split('\\n\\r\\n')
        if len(data_str) > 1:
            dataLimit = [x for x in data_str[2:] if x != 'n']
            return np.array([float(x) for x in dataLimit])

    def __del__(self):
        self.disconnect()

class FileHandler(DataAcquirer):

    def __init__(self, file_path: str):
        self.data = None
        self.file = self._read_file(file_path)
        self.line_counter = 0

    def _read_file(self, file_path) -> list:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip() and line.strip() != 'n']  # Remove empty lines and lines equal to 'n'
        return lines
    
    def _read_line(self) -> str:
        """Read a line from the file."""
        line = self.file[self.line_counter]
        self.line_counter += 1
        if self.line_counter >= len(self.file):
            self.line_counter = 0
        return line

    def _parse_data_from_file(self, source: str) -> np.ndarray:
        """Process the raw data string into a list of floats."""
        dataStr = source.split(' ')
        if len(dataStr) > 1:
            dataLimit = [x for x in dataStr[2:]] # eliminate the extra ('I' 'got') in div_str; make the string to be float
            return np.array([float(x) for x in dataLimit])
        else:
            raise ValueError("Data string is not in the expected format.")
        
    def connect(self):
        pass

    def disconnect(self):
        pass

    def acquire_data(self) -> np.ndarray:
        data = self._read_line()
        return self._parse_data_from_file(data)
