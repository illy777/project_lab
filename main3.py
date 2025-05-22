#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from pipelines.registry import *
from app.builder import *
from gui.visualizer import *
from PyQt6.QtWidgets import QApplication
import sys
    

if __name__ == "__main__":
    # Example usage

    mesh_types = Pipeline_Registry().get_meshtypes()
    app = QApplication(sys.argv)
    gui = Gui(mesh_types=mesh_types)
    gui.resize(1200, 700)
    gui.show()



    sys.exit(app.exec())

    #while True:
     #   data = pipeline.do_measurement()
      #  plotter.eitplot(ds=data, el_pos=pipeline.mesh.el_pos, mesh_obj=pipeline.mesh.meshObject)
    #plotter.start.clicked.connect(object_value)
    
    
