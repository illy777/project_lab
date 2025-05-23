from enum import StrEnum, Enum

class MeshType(StrEnum):
    circularMesh = "circular",
    forearmMesh = "forearm",
    lungMesh = "lung"

class InjectionPattern(Enum):
    adjacent = 0,
    opposite = 1,
    skip3 = 2,
    rotatingRadial = 3

class ReconstructionAlgorithm(Enum):
    pipeline = 0,
    gaussNewton = 1