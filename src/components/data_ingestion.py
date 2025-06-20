import os
import sys
import pandas as pd
import logging
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingest_config=DataIngestionConfig()
        logging.info("Data Ingestion Initiated")

    def ingest_data_from_source(self):
        """
        This collects data from source, reads it as DataFrame
        and stores a corresponding csv file for the raw data.
        It also splits the raw csv into train and test csv files
        All 3 csv files present in the artifacts folder of this project package.
        """
        try:
            df=pd.read_csv(os.path.join("notebook","data","stdnt_perf.csv"))
        except Exception as e:
            logging.info("Conversion of source data to dataframe failed")
            raise CustomException(e,sys)
        else:
            logging.info("Successfully converted the data from source into a pandas DataFrame")
        
        os.makedirs(os.path.dirname(self.ingest_config.raw_data_path),exist_ok=True)
        
        try:
            df.to_csv(self.ingest_config.raw_data_path,index=False,header=True)
        except Exception as e:
            logging.info("Exception Occured,Could not create raw data file")
            raise CustomException(e,sys)
        else:
            logging.info("DataFrame moved to raw_data_path")

        train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
        logging.info("Raw Data Split into train and test")

        try:
            train_set.to_csv(self.ingest_config.train_data_path,index=False,header=True)
        except Exception as e:
            logging.info("Exception Occured,Could not create train data file")
            raise CustomException(e,sys)
        else:
            logging.info("Train set moved to train_data_path")
        
        try:
            test_set.to_csv(self.ingest_config.test_data_path,index=False,header=True)
        except Exception as e:
            logging.info("Exception Occured,Could not create train data file")
            raise CustomException(e,sys)
        else:
            logging.info("Test set moved to test_data_path")

        return(
            self.ingest_config.raw_data_path,
            self.ingest_config.train_data_path,
            self.ingest_config.test_data_path
        )

if __name__=="__main__":
    ingestion_obj=DataIngestion()
    ingestion_obj.ingest_data_from_source()
        


