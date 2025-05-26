# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
#
# Descritpion: This module is a part of the application that handles the circular mesh generation and data processing pipeline.
# It relies on the framework in the data_processing module.

from pipelines.circular_mesh import *
from app.app import RegistryInterface

class PipelineRegistry(RegistryInterface):
    def __init__(self):
        self._meshoptions = {"circular": self._choose_circular}

    def get_meshtypes(self) -> list[str]:
        return list(self._meshoptions.keys())

    def _choose_circular(self, n_el: int, h0: float, *args):
        return CircularMeshPipeline(n_el=n_el, h0=h0)