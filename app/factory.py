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

    def load_model(self, model_name: str, model_file: str, load_function: callable):
        path = os.path.join(os.getcwd(),"pipelines","models")
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, model_file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file {model_file} not found in {path}.")
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

class Data_Acquirer(ABC):
    @abstractmethod
    def acquire_data(self) -> np.ndarray:
        """This method should be implemented in the derived class."""
        pass

class Pipeline:
    def __init__(self, mesh):
        self.mesh = mesh
        self.data_interface = None
    
    @abstractmethod
    def evaluate_data(self, data: np.ndarray) -> np.ndarray:
        """This method should be implemented in the derived class."""
        pass
    
    def do_measurement(self) -> np.ndarray:
        data = self.data_interface.acquire_data()
        return self.evaluate_data(data)
    
    def set_data_interface(self, data_interface: Data_Acquirer):
        if data_interface is None:
            raise ValueError("Data interface is not set. Please set the data interface before using it.")
        self.data_interface = data_interface
