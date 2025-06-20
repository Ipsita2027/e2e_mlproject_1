import pandas as pd
import os
import sys
import numpy as np
import src.utils as utils
from src.logger import logging
from src.exception import CustomException
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str=os.path.join(".","artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_trans_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            #segragating cat and num columns, refer: notebook/EDA_STUDENT_PERFORMANCE
            num_features=["writing_score","reading_score"]
            cat_features=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            #numerical pipeline
            num_pipeline_obj=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            #categorical pipeline
            cat_pipeline_obj=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("onehotencoder",OneHotEncoder())
                ]
            )

            logging.info("Initializing column transformer")

            preprocessor=ColumnTransformer(
                [
                ("numerical_pipeline",num_pipeline_obj,num_features),
                ("categorical_pipeline",cat_pipeline_obj,cat_features)
                ]
            )
        except Exception as e:
            raise CustomException(e,sys)
        
        return preprocessor
        

    def initiate_data_transformation(self,train_data,test_data):
        try:
            df_train=pd.read_csv(train_data)
            df_test=pd.read_csv(test_data)
        except Exception as e:
            logging.info("Error occured while reading train and test csv files")
            raise CustomException(e,sys)
        else:
            logging.info("Successfully read train and test datasets")
    
        preprocessor_obj=self.get_data_transformer_object()

        logging.info("Transformation of train and test columns begins")

        #get labels
        y_train=df_train["math_score"]
        y_test=df_test["math_score"]
        df_train=df_train.drop(columns=["math_score"])
        df_test=df_test.drop(columns=["math_score"])

        pre_train_arr=preprocessor_obj.fit_transform(df_train)
        pre_test_arr=preprocessor_obj.fit_transform(df_test)

        logging.info("The numerical columns standardized")
        logging.info("Categorical columns one hot encoded")


        train_arr=np.c_[pre_train_arr,np.array(y_train)]
        test_arr=np.c_[pre_test_arr,np.array(y_test)]

        logging.info("Saving the transformer object as a pickle file")

        utils.save_object(
            file_path=self.data_trans_config.preprocessor_obj_file_path,
            obj=preprocessor_obj
        )

        logging.info("Column Transformer object saved as pickle file")

        return (
            train_arr,
            test_arr,
            self.data_trans_config.preprocessor_obj_file_path
        )

