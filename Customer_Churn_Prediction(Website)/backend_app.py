from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

#loading the lightGBM model from saved in jupyter
model = joblib.load('lgbm_churn_model.joblib')

#create instance of api
app = FastAPI()

#define input schema using pydantic
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    InternetService_DSL: int
    InternetService_Fiber_optic: int
    OnlineSecurity_No: int
    OnlineSecurity_Yes: int
    TechSupport_No: int
    TechSupport_Yes: int
    Contract_One_year: int
    Contract_Two_year: int

#define prediction route
@app.post("/predict")
def predict(data:CustomerData):

    #input to dataframe
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])

    #predict
    proba = model.predict_proba(df)[0][1]
    prediction = model.predict(df)[0]

    #returning result
    return {
        "churn_probability": round(proba, 4),
        "prediction": "Yes" if prediction == 1 else "No"
    }