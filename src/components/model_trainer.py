import sys
import os
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from src.logger import logging
from src.utils import train_and_evaluate_models,save_object
from src.exception import CustomException
from dataclasses import dataclass
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

@dataclass
class ModelTrainerConfig:
    trained_model_path=os.path.join(".","artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        logging.info("Model Training initiated")

        X_train,X_test,y_train,y_test=(
            train_arr[:,:-1],
            test_arr[:,:-1],
            train_arr[:,-1],
            test_arr[:,-1]
        )

        logging.info("Labels and Features separated from transformed data for train and test")

        models={
            "linearegression":LinearRegression(),
            "ridge":Ridge(),
            "lasso":Lasso(),
            "decisiontree":DecisionTreeRegressor(),
            "randomforest":RandomForestRegressor(),
            "adaboost":AdaBoostRegressor(),
            "xgboost":XGBRegressor(),
            "knebors":KNeighborsRegressor(n_neighbors=5)
        }

        logging.info("Training starts")

        r2_train,r2_test = train_and_evaluate_models(models,X_train,X_test,y_train,y_test)

        logging.info("All models successfully trained")

        logging.info("Plotting the r2 scores of all the models")

        plt.figure(figsize=(10,4))
        plt.plot([model for model in models],r2_train,marker="o",color="blue",label="train dataset")
        plt.plot([model for model in models],r2_test,marker="o",color="red",label="test dataset")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(".","artifacts","r2_scores.png"))
        plt.close()

        logging.info("A file for the plot is saved")

        indx=r2_test.index(max(r2_test))

        best_model_name=list(models.keys())[indx]
        if r2_test[indx]<=0.6:
            logging.info("None of the models upto the mark")
        else:
            logging.info("The best model was {best_model_name} with r2 score of {r2_test[indx]} in test data")
            logging.info("Saving the model as pickel file")

            model=models[best_model_name]

            try:
                save_object(self.model_trainer_config.trained_model_path,model)
            except  Exception as e:
                logging.info("Model could not be saved,Exception occured")
                raise CustomException(e,sys)

        
