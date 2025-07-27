from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal 
import numpy as np
import pickle
import pandas as pd

import sklearn
from pydantic import BaseModel, Field, computed_field


app = FastAPI()

# we are Fist Importing the Our ML Model

with open('model_1.pkl', 'rb') as file:
    model=pickle.load(file)


    tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",    "Pune"]
        
    tier_2_cities = [
   "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore","Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal","Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri" ]




# fist we are creating a Pydantic model for the input data

class UserInput(BaseModel):

    age: int = Field(...,gt=0,le=120,description="Age of the user")
    weight: float = Field(...,gt=0,description="Weight of the user in kg")
    height: float = Field(...,gt=0,description="Height of the user in cm")
    income_lpa: float = Field(...,gt=0,description="Income of the user in lakhs per annum")
    smoker: Literal['yes', 'no'] = Field(...,description="Smoking status of the user")
    city: str = Field(...,description="City of the user")
    occupation:Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'] = Field(...,description="Occupation of the user")
    




# 1st Computed Field

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height / 100)**2
    
# 2nd Computed Field
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
       
       if self.smoker == 'yes' and self.bmi > 30:
          return "high"
       elif self.smoker == 'yes' or self.bmi > 27:
          return "medium"
       else:
          return "low" 
       
# 3rd Computed Field

    @computed_field
    @property
    def age_group(self) -> str:

        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    
# 4th Computed Field

    @computed_field
    @property

    def city_tier(self) -> int:

        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3




## Now we are Building the API Endpoint

@app.post("/predict")
def predict_premium(data : UserInput):

    input_df = pd.DataFrame([{

        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }]) 




    model_prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'Predicted_Category': model_prediction})
