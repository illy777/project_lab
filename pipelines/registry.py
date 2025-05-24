# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#
# Descritpion: This module is a part of the application that handles the circular mesh generation and data processing pipeline.
# It relies on the framework in the data_processing module.

from pipelines.circular_mesh import *
from app.data_types import MeshType

class PipelineRegistry():
    def __init__(self):
        self._meshoptions = {MeshType.circularMesh: self._choose_circular}

    def get_meshtypes(self) -> list[MeshType]:
        return list(self._meshoptions.keys())

    def _choose_circular(self, n_el: int, h0: float, *args):
        return CircularMeshPipeline(n_el=n_el, h0=h0)