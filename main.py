#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from pipelines.registry import *
from app.measurement import *
from app.adapters import *
from gui.plot import *
from PyQt5.QtWidgets import QApplication
import sys
    

if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)
    plotter = PLOT()

    registry = Pipe_Registry()
    registred_pipes = registry.get_meshtypes()

    measurement = Measurement(meshtype="circular", n_el=8, h0=0.07, maxArea=None, registry=registry)
    measurement_interface = FileHandler()
    interface_adapter = InputAdapter()


    data_list = measurement_interface.readFile("simulation/simulation.txt")
    plotter.show()
    for data in data_list:
        data = interface_adapter.parse_data_from_file(data)
        data = measurement.do_measurement(data)
        plotter.eitplot(ds=data, el_pos=measurement.mesh.el_pos, mesh_obj=measurement.mesh.meshObject)
    #plotter.start.clicked.connect(object_value)
    sys.exit(app.exec_())
