#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the measurement registry for the EIT system.

from app.circular_mesh import *

MESHOPTIONS = ["circular"]

class Measurement():
    def __init__(self, meshtype: str, n_el: int = None, h0: float = None, maxArea: float= None):
        self.meshtype = meshtype
        self.mesh = None
        self.measurement = None
        if not self._validate_meshtype():
            raise ValueError(f"Invalid meshtype: {self.meshtype}")
        self._choose_measurement(n_el, h0, maxArea)
        if not callable(self.measurement.do_measurement):
            raise ValueError("Measurement method is not callable. Please implement the method do_measurement(self, data:np.ndarray)-> np.ndarray in the measurement class.")
        
    def _validate_meshtype(self):
        if(self.meshtype not in MESHOPTIONS):
            return False
        return True

    def _choose_circular(self, n_el: int, h0: float) -> CircularMeshPipeline:
        self.mesh = CircularMesh(n_el=n_el, h0=h0)
        self.measurement = CircularMeshPipeline()

    def _choose_measurement(self, n_el: int, h0: float, maxArea: float):
        if self.meshtype == "circular":
            self._choose_circular(n_el, h0)
        else:
            raise ValueError(f"Unknown meshtype: {self.meshtype}")

    def do_measurement(self, data:np.ndarray) -> np.ndarray:
        return self.measurement.do_measurement(data)
    
