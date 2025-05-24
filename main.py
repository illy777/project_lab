#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from pipelines.registry import *
from app.builder import *
from gui.gui import Gui
from PyQt6.QtWidgets import QApplication
import sys
import threading
from app.overseer import Overseer

    

if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)

    data_acquirer = FileHandler("simulation/simulation.txt")
    gui = Gui()
    pipeline_builder =  PipelineBuilder()
    registry = PipelineRegistry()
    gui.resize(1200, 700)
    gui.show()

    overseer = Overseer(gui, data_acquirer, pipeline_builder, registry)
    overseerThread = threading.Thread(target=overseer.exec, daemon=True)
    overseerThread.start()

    sys.exit(app.exec())

