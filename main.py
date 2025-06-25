# Copyright (c) 2025
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>

# Descritpion: This module contains the main application logic for the EIT measurement system.

from app.data_acquire import *
from app.builder import *
from gui.gui import Gui
from gui.adapter import GuiAdapter
from PyQt6.QtWidgets import QApplication
import sys
import threading
from app.app import Sentinel



if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)

    data_acquirer = FileHandler("simulation/simulation.txt")
    gui = Gui()
    registry = PipelineRegistry()
    pipeline_builder =  PipelineBuilder(registry)
    gui.showMaximized()
    gui.show()
    gui_adapter = GuiAdapter(gui)

    # automatically starts the backend thread during creation of Sentinel
    sentinel = Sentinel(gui_adapter, data_acquirer, pipeline_builder, registry)

    sys.exit(app.exec())
