#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from pipelines.registry import *
from app.builder import *
from gui.visualizer import *
from PyQt6.QtWidgets import QApplication
import sys
import threading
    

if __name__ == "__main__":
    # Example usage

    mesh_types = Pipeline_Registry().get_meshtypes()
    app = QApplication(sys.argv)
    gui = Gui(mesh_types=mesh_types)
    gui.resize(1200, 700)
    gui.show()
    app.exec()
    #gui_thread = threading.Thread(target=app.exec(), daemon=True)

    meshtype = gui.get_mesh_type()
    n_el = gui.get_n_electrodes()
    h0 = gui.get_h0()
    el_pos = gui.get_el_pos()
  
    if gui.run_button.isChecked():
        data_interface = FileHandler("simulation/simulation.txt")
        pipeline = Pipeline_Builder().build_pipeline(meshtype, n_el, h0, maxArea=None, data_interface=data_interface) 

        loop_count = 0
        while gui.run_button.isChecked():
            data = pipeline.do_measurement()
            voltages = data_interface.get_raw_data()
            gui.heatmap_display.update_heatmap_opencv(ds=data, el_pos=pipeline.mesh.el_pos, mesh_obj=pipeline.mesh.meshObject)
            gui.heatmap_display.show()
            anomaly_position = pipeline.get_anomaly_position()
            # --- NEW: Update the real-time plot with voltage data from file ---
            try:
              gui.plot_canvas.set_voltage_data_from_file(voltages)
            except Exception as e:
                gui.log_message(f"[ERROR] Could not update Voltage vs. Time plot: {e}")
            if loop_count % 3 == 0:
                gui.log_message(f"Predicted anomaly region: {anomaly_position}") #show predicted region every 3 iterations
            loop_count += 1
    sys.exit()

    #while True:
     #   data = pipeline.do_measurement()
      #  plotter.eitplot(ds=data, el_pos=pipeline.mesh.el_pos, mesh_obj=pipeline.mesh.meshObject)
    #plotter.start.clicked.connect(object_value)


