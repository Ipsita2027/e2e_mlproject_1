# Responsible for transforming form data into a dataframe
#and then load the preprocessor and model from .pkl files
#and return the prediction to the app.py
import sys
import os
from src.exception import CustomException
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,df):
        model_path=os.path.join(".","artifacts","model.pkl")
        preprocessor_path=os.path.join(".","artifacts","preprocessor.pkl")
        try:
            preprocessor_obj=load_object(preprocessor_path)
            pred_array=preprocessor_obj.transform(df)
            model=load_object(model_path)
            return model.predict(pred_array)
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
                 gender:str,
                 ethnicity:str,
                 parental_education:str,
                 lunch:str,
                 test_preparation_course:str,
                 reading_score:int,
                 writing_score:int):
        self.gender=gender
        self.ethnicity=ethnicity
        self.parental_education=parental_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=reading_score
        self.writing_score=writing_score

    def create_dataframe(self):
        try:
            data={
                "gender":[self.gender],
                "race_ethnicity":[self.ethnicity],
                "parental_level_of_education":[self.parental_education],
                "lunch":[self.lunch],
                "test_preparation_course":[self.test_preparation_course],
                "reading_score":[self.reading_score],
                "writing_score":[self.writing_score]
            }
        except Exception as e:
            raise CustomException(e,sys)
        try:
            return pd.DataFrame(data=data)
        except Exception as e:
            raise CustomException(e,sys)
    
    