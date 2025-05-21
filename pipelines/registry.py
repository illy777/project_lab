#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module is a part of the application that handles the circular mesh generation and data processing pipeline.
#It relies on the framework in the data_processing module.

from pipelines.circular_mesh import *

class Pipeline_Registry():
    def __init__(self):
        self.meshoptions = {"circular": self._choose_circular}

    def get_meshtypes(self):
        return list(self.meshoptions.keys())

    def _choose_circular(self, n_el: int, h0: float, *args):
        return CircularMeshPipeline(n_el=n_el, h0=h0)