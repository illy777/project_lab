#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from app.measurement_registry import *
from app.adapters import *
from gui.visualizer import Visualizer
from PyQt6.QtWidgets import QApplication
import sys
import os

if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)
    gui = Visualizer()
    gui.resize(1200, 700)
    gui.show()
    
    # heatmap = gui.heatmap_display

    meshtype = gui.get_mesh_type()
    n_el = gui.get_n_electrodes()
    h0 = gui.get_h0()
    
    #measurement = Measurement(meshtype,n_el,h0, maxArea=None)
    #measurement_interface = FileHandler()
    #interface_adapter = InputAdapter()

    model_path = os.path.join("app", "models", "gp_model_new_1_0.001.pkl")

    #data = measurement_interface.readFile("simulation/simulation.txt")
    #print(data)
    #data = interface_adapter.parse_data_from_file(data[0])
    #result = measurement.do_measurement(data)

    sys.exit(app.exec())