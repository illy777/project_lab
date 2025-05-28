# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Thomas Harald Reinhard RUBIN <thomas.rubin2@protonmail.com>
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#
# Descritpion: Data types for the EIT measurement system.


from enum import StrEnum, IntEnum


class ElectrodeNumber(IntEnum):
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32
    SIXTY_FOUR = 64

    def __str__(self):
        return str(self.value)
    
    def __int__(self):
        return self.value

class InjectionPattern(StrEnum):
    ADJACENT = "adjacent",
    OPPOSITE = "opposite",
    SKIP3 = "skip3",
    ROTATING_RADIAL = "rotatingRadial"
    
    def __str__(self):
        return self.value
    
    def __int__(self):
        return self.value
    
class Baudrate(IntEnum):
    B9600 = 9600
    B19200 = 19200
    B38400 = 38400
    B57600 = 57600
    B115200 = 115200
    B230400 = 230400
    B460800 = 460800
    B921600 = 921600

    def __str__(self):
        return str(self.value)
    
    def __int__(self):
        return self.value