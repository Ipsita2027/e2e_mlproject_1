##This module will handle the submitted variable values by the
#user in the ui page and the collected data will interact
#with the preprocessor and model pickle files

#BACKEND LOGIC 

import numpy as np
import pandas as pd
from flask import Flask,request,render_template
from src.pipelines.predict_pipeline import CustomData,PredictPipeline

app=Flask(__name__)

@app.route("/")
def get_home_page():
    return render_template("home.html")

@app.route("/predictdata",methods=["GET","POST"])
def predict_data_post():
    if request.method=="GET":
        return render_template("form.html")
    else:
        #collect the form data and send it to predictin pipeline
        data=CustomData(
            gender=request.form.get("gender"),
            ethnicity=request.form.get("race_ethnicity"),
            parental_education=request.form.get("parental_education"),
            lunch=request.form.get("lunch"),
            test_preparation_course=request.form.get("test_preparation_course"),
            reading_score=request.form.get("reading_score"),
            writing_score=request.form.get("writing_score")
        )
        pred_df=data.create_dataframe()
        predict_pipeline=PredictPipeline()
        y_hat=predict_pipeline.predict(pred_df)
        return render_template("form.html",result=int(y_hat[0]))

if __name__=="__main__":
    app.run(host="127.0.0.1",port=4000,debug=True)

