import numpy as np
import os
import dill
import sys
import pandas as pd
from src.exception import CustomException
from sklearn.metrics import r2_score

def save_object(file_path=None,obj=None):
    if file_path and obj:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        try:
            with open(file_path,"wb") as file:
                dill.dump(obj,file)
        except Exception as e:
            raise CustomException(e,sys)
        

def train_and_evaluate_models(models,X_train,X_test,y_train,y_test):
    models_list=list(models.keys())
    r2_scores_train=[]
    r2_scores_test=[]

    def model_training(model):
        model.fit(X_train,y_train)
        y_train_pred=model.predict(X_train)
        r2_scores_train.append(r2_score(y_train,y_train_pred))
        y_test_pred=model.predict(X_test)
        r2_scores_test.append(r2_score(y_test,y_test_pred))

    for i in range(len(models_list)):
        model_training(models[models_list[i]])

    return (r2_scores_train,r2_scores_test)