from fastapi import FastAPI
from fastapi.responses import JSONResponse

from Schema.user_input import UserInput
from Schema.prediction_response import PredictionResponse
from model.predict import predict_output,model, MODEL_VERSION


app = FastAPI()

      
@app.get("/")
def home():
        return {"message": "Welcome to the Insurance Premium Prediction API"}


@app.get("/health")
def health_check():
    return {
        "status":"Ok",
        "version":MODEL_VERSION,
        "model_loaded": model is not None
        }


## Now we are Building the API Endpoint

@app.post("/predict" , response_model=PredictionResponse)
def predict_premium(data : UserInput):

    user_input ={
         
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation

    }

    try:
        
        prediction = predict_output(user_input)
        return JSONResponse(content={"Predicted_Category": prediction})
    
    except Exception as e:

        return JSONResponse(content={"error": str(e)}, status_code=500)  
         


 