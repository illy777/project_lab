# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#
# Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from pipelines.registry import *
from app.builder import *
from gui.plot import *
from PyQt5.QtWidgets import QApplication
import sys
    

if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)
    plotter = PLOT()

    registred_pipes = Pipeline_Registry().get_meshtypes()
    data_interface = FileHandler("simulation/simulation.txt")
    pipeline = Pipeline_Builder().build_pipeline(meshtype='circular', n_el=8, h0=0.07, maxArea=None, data_interface=data_interface)

    plotter.show()
    while True:
        data = pipeline.do_measurement()
        plotter.eitplot(ds=data, el_pos=pipeline.mesh.el_pos, mesh_obj=pipeline.mesh.meshObject)
    #plotter.start.clicked.connect(object_value)
    sys.exit(app.exec_())
