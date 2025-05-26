# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Thomas Harald Reinhard RUBIN <thomas.rubin2@protonmail.com>
#
# Descritpion: Data types for the EIT measurement system.


from enum import StrEnum, Enum


class ElectrodeNumber(Enum):
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