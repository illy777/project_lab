# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
#
# Descritpion: This module contains a class for acquiring data from the serial port for this specific application.

import serial
import serial.tools.list_ports
import numpy as np
from app.app import DataAcquirerInterface
from app.data_types import *
import time
class Parser():

    @staticmethod
    def _is_float(value: str) -> bool:
        """Check if a string can be converted to a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_data(source: str) -> np.ndarray:
        """Process the raw data string into a list of floats."""
        data_str = source.split('\\n')
        data_str = data_str[0].split('\\r')
        data_str = data_str[0]
        if isinstance(data_str, list) or data_str is None:
            raise ValueError("Parsed data_str is invalid.")
        data_str = data_str.split(' ')
        data = [x for x in data_str if Parser()._is_float(x)] 
        if data is None or len(data) == 0:
            raise ValueError("Parsed data is invalid.")
        return np.array([float(x) for x in data])
        
class SerialPort(DataAcquirerInterface):
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serialConnection = None

    def connect(self):
        if self.serialConnection and self.serialConnection.is_open:
            self.disconnect()
        self.serialConnection = serial.Serial(self.port, self.baudrate)
        time.sleep(0.1)  # wait for connection to stabilize
        self.send_byte(1)

    def disconnect(self):
        if self.serialConnection and self.serialConnection.is_open:
            self.serialConnection.close()

    def _read_data(self):
        """Read raw data string from serial until end marker is found."""
        dataStr = ""
        self.send_byte(1)
        while not ('\\r\\n' in dataStr):
            dataByte = self.serialConnection.read(self.serialConnection.inWaiting())
            if len(dataByte) > 0:
                dataStr += str(dataByte).split("'")[1]
        return dataStr

    def send_byte(self, data: bytes):
        """Send bytes to the serial port."""
        if self.serialConnection and self.serialConnection.is_open:
            self.serialConnection.write(data)
        else:
            raise ConnectionError("Serial port is not connected.")

    def acquire_data(self) -> np.ndarray:
        data = self._read_data()
        return Parser.parse_data(data)

    def get_available_baudrates(self) -> list[int]:
        """Return a list of common baud rates."""
        return [baudrate.value for baudrate in Baudrate]

    def get_serial_ports(self) -> list[str]:
        """Return a list of available serial ports."""
        return [port.device for port in serial.tools.list_ports.comports()]

    def set_serial_port(self, port: str):
        """Set the serial port to connect to."""
        self.port = port
    
    def set_baudrate(self, baudrate: int):
        """Set the baud rate for the serial connection."""
        self.baudrate = baudrate

    def __del__(self):
        self.disconnect()

class FileHandler(DataAcquirerInterface):

    def __init__(self, file_path: str):
        self.data = None
        self.file = self._read_file(file_path)
        self._line_counter = 0

    def _read_file(self, file_path) -> list:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip() and line.strip() != 'n']  # Remove empty lines and lines equal to 'n'
        return lines
    
    def _read_line(self) -> str:
        """Read a line from the file."""
        line = self.file[self._line_counter]
        self._line_counter += 1
        if self._line_counter >= len(self.file):
            self._line_counter = 0
        return line

    def connect(self):
        pass

    def disconnect(self):
        self._line_counter = 0

    def get_available_baudrates(self) -> list[int]:
        return []

    def get_serial_ports(self) -> list[str]:
       return []

    def set_serial_port(self, port: str):
        pass

    def set_baudrate(self, baudrate: int):
        pass

    def acquire_data(self) -> np.ndarray:
        data = self._read_line()
        return Parser.parse_data(data)