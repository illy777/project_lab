# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
#
# Descritpion: This module contains a class for acquiring data from the serial port for this specific application.

import serial
import numpy as np
from app.app import DataAcquirerInterface

class DataAcquirer():
    def _parse_data(self, source: str) -> np.ndarray:
        """Process the raw data string into a list of floats."""
        data_str = source.split('\\n')
        data_str = data_str[0].split('\\r')
        data_str = data_str[0]
        if isinstance(data_str, list) or data_str is None:
            raise ValueError("Parsed data_str is invalid.")
        data_str = data_str.split(' ')
        data = [x for x in data_str if self._is_float(x)] 
        if data is None or len(data) == 0:
            raise ValueError("Parsed data is invalid.")
        return np.array([float(x) for x in data])

    def _is_float(self, value: str) -> bool:
        """Check if a string can be converted to a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
        
class SerialPort(DataAcquirerInterface, DataAcquirer):
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serialConnection = None

    def connect(self):
        self.serialConnection = serial.Serial(self.port, self.baudrate)
        self.serialConnection.write(bytes(1))

    def disconnect(self):
        if self.serialConnection and self.serialConnection.is_open:
            self.serialConnection.close()

    def _read_data(self):
        """Read raw data string from serial until end marker is found."""
        dataStr = ""
        self.serialConnection.write(bytes(1))
        while not ('\\r\\n' in dataStr):
            dataByte = self.serialConnection.read(self.serialConnection.inWaiting())
            if len(dataByte) > 0:
                dataStr += str(dataByte).split("'")[1]
        return dataStr

    def acquire_data(self) -> np.ndarray:
        data = self._read_data()
        return self._parse_data(data)

    def get_available_baudrates(self) -> list[int]:
        """Return a list of common baud rates."""
        return [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 230400, 250000, 500000, 1000000]

    def get_serial_ports(self) -> list[str]:
        """Return a list of available serial ports."""
        return [port.device for port in serial.tools.list_ports.comports()]

    def set_serial_port(self, port: str):
        """Set the serial port to connect to."""
        self.port = port
        if self.serialConnection and self.serialConnection.is_open:
            self.disconnect()
        self.connect()
    
    def set_baudrate(self, baudrate: int):
        """Set the baud rate for the serial connection."""
        self.baudrate = baudrate
        if self.serialConnection and self.serialConnection.is_open:
            self.disconnect()
        self.connect()

    def __del__(self):
        self.disconnect()

class FileHandler(DataAcquirerInterface, DataAcquirer):

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

    def connect(self):
        pass

    def disconnect(self):
        pass

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
        return self._parse_data(data)
