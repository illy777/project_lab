#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the foundation for the data pipeline, including the mesh generation and model loading.

import numpy as np
import os
from abc import ABC, abstractmethod

class Mesh:
    @abstractmethod
    def generate_mesh(self, **kwargs):
        """This method should be implemented in the derived class."""
        pass

class Model:
    def __init__ (self):
        self.compensation_model = None
        self.region_model = None
        self.reconstruction_model = None
        self.denoising_model = None

    def load_model(self, model_name: str, model_path: str, load_function: callable):
        path = os.path.join(os.getcwd(), model_path)
        if model_name == "compensation":
            self.compensation_model = load_function(path)
        elif model_name == "region":
            self.region_model = load_function(path)
        elif model_name == "reconstruction":
            self.reconstruction_model = load_function(path)
        elif model_name == "denoising":
            self.denoising_model = load_function(path)
        else:
            raise ValueError(f"Unknown model name: {model_name}")


class Pipeline:
    def __init__(self, mesh = None):
        self.mesh = mesh
        if self.mesh is None:
            raise ValueError("Mesh is not provided. Please provide a valid mesh.")
    
    @abstractmethod
    def do_measurement(self, data: np.ndarray) -> np.ndarray:
        """This method should be implemented in the derived class."""
        pass