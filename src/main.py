from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from prediction_model.predict import generate_predictions

app=FastAPI(title="loan predict app",version='1.0')

origins=["*"]

app.add_middleware(CORSMiddleware,allow_origins=origins,
                   allow_credentials=True,allow_methods=["*"],
                   allow_headers=["*"])

class LoanPrediction(BaseModel):
    Gender:str
    Married:str
    Dependents:str
    Education:str
    Self_Employed:str
    ApplicantIncome:float
    CoapplicantIncome:float
    LoanAmount:float
    Loan_Amount_Term:float
    Credit_History:float
    Property_Area:str


@app.get("/")
def index():
    return{"message":"loan predict app jenkin"}

@app.post("/prediction_api")
def predict(loan_details: LoanPrediction):
    data=loan_details.model_dump()
    prediction=generate_predictions([data])['prediction'][0]
    if prediction=="Y":
        pred ="Approved"
    else:
        pred ="rejected"
    return {'status':pred}

@app.post("/prediction_ui")
def predict_gui(Gender:str,
    Married:str,
    Dependents:str,
    Education:str,
    Self_Employed:str,
    ApplicantIncome:float,
    CoapplicantIncome:float,
    LoanAmount:float,
    Loan_Amount_Term:float,
    Credit_History:float,
    Property_Area:str):
    
    input_data=[Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area]

    cols=['Gender', 'Married', 'Dependents', 'Education',
       'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    
    data_dict=dict(zip(cols,input_data))

    prediction=generate_predictions([data_dict])['prediction'][0]
    if prediction=="Y":
        pred ="Approved"
    else:
        pred ="rejected"
    return {'status':pred}


if __name__=="__main__":
    uvicorn.run(app)