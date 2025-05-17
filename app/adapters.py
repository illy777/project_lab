#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains all adapters for the application that will intereract with the GUI and the data pipeline.

import numpy as np

class InputAdapter:

    def parse_data_from_file(self, source: str) -> np.ndarray:
        """Process the raw data string into a list of floats."""
        dataStr = source.split(' ')
        if len(dataStr) > 1:
            dataLimit = [x for x in dataStr[2:]] # eliminate the extra ('I' 'got') in div_str; make the string to be float
            return np.array([float(x) for x in dataLimit])
        else:
            raise ValueError("Data string is not in the expected format.")