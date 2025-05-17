#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from app.measurement_registry import *
from app.adapters import *
from gui.plot import *
from PyQt5.QtWidgets import QApplication
import sys
    

if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)
    plotter = PLOT()

    measurement = Measurement(meshtype="circular", n_el=8, h0=0.07, maxArea=None)
    measurement_interface = FileHandler()
    interface_adapter = InputAdapter()


    data = measurement_interface.readFile("simulation/simulation.txt")
    data = interface_adapter.parse_data_from_file(data[0])
    result = measurement.do_measurement(data)

    plotter.eitplot(ds=result, el_pos=measurement.mesh.el_pos, mesh_obj=measurement.mesh.meshObject)
    plotter.show()
    #plotter.start.clicked.connect(object_vaule)
    sys.exit(app.exec_())
