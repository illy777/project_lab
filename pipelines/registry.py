#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module is a part of the application that handles the circular mesh generation and data processing pipeline.
#It relies on the framework in the data_processing module.

from pipelines.circular_mesh import *

class Choice():
    def __init__(self, mesh=None, measurement=None):
        self.mesh = mesh
        self.measurement = measurement

class Pipe_Registry():
    def __init__(self):
        self.meshoptions = {"circular": self._choose_circular}

    def get_meshtypes(self):
        return list(self.meshoptions.keys())

    def _choose_circular(self, n_el: int, h0: float, *args) -> Choice:
        mesh = CircularMesh(n_el=n_el, h0=h0)
        measurement = CircularMeshPipeline()
        return Choice(mesh=mesh, measurement=measurement)