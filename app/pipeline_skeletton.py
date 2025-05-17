#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the foundation for the data pipeline, including the mesh generation and model loading.

import numpy as np
import os

class Mesh:
    def __init__(self, n_el: int = None, h0: float = None, maxArea: float = None):
        self.numberElectrodes: int = n_el
        self.h0: float = h0 #here we need a better naming
        self.maxArea: float = maxArea
        self.meshObject: dict = None

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

class DataPipeline:
    def __init__(self):
        self.input : np.ndarray = []
        self.output : np.ndarray = []

    def load_data(self, source: np.ndarray):
        self.input = source


