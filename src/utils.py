import numpy as np
import os
import dill
import sys
import pandas as pd
from src.exception import CustomException

def save_object(file_path=None,obj=None):
    if file_path and obj:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        try:
            with open(file_path,"wb") as file:
                dill.dump(obj,file)
        except Exception as e:
            raise CustomException(e,sys)
        