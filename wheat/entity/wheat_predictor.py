import os
import sys

from wheat.exception import WheatException
from wheat.util.util import load_object

import pandas as pd


class WheatData:

    def __init__(self,
                 Area: float,
                 Perimeter: float,
                 Compactness: float,
                 Kernel_Length: float,
                 Kernel_Width: float,
                 Asymmetry_Coeff: float,
                 Kernel_Groove: float,
                 Type: int = None
                 ):
        try:
            self.Area = Area
            self.Perimeter = Perimeter
            self.Compactness = Compactness
            self.Kernel_Length = Kernel_Length
            self.Kernel_Width = Kernel_Width
            self.Asymmetry_Coeff = Asymmetry_Coeff
            self.Kernel_Groove = Kernel_Groove
            self.Type = Type
        except Exception as e:
            raise WheatException(e, sys) from e

    def get_wheat_input_data_frame(self):

        try:
            wheat_input_dict = self.get_wheat_data_as_dict()
            return pd.DataFrame(wheat_input_dict)
        except Exception as e:
            raise WheatException(e, sys) from e

    def get_wheat_data_as_dict(self):
        try:
            input_data = {
                "Area": [self.Area],
                "Perimeter": [self.Perimeter],
                "Compactness": [self.Compactness],
                "Kernel_Length": [self.Kernel_Length],
                "Kernel_Width": [self.Kernel_Width],
                "Asymmetry_Coeff": [self.Asymmetry_Coeff],
                "Kernel_Groove": [self.Kernel_Groove]}
            return input_data
        except Exception as e:
            raise WheatException(e, sys)


class WheatClassifier:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise WheatException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise WheatException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise WheatException(e, sys) from e