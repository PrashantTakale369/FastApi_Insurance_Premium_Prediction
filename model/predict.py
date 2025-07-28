import pandas as pd
import pickle



# we are Fist Importing the Our ML Model

with open('model\model_1.pkl', 'rb') as file:
    model=pickle.load(file)

MODEL_VERSION = "1.0.0"



# We are extracting the class labels from the model
classes_labels = model.classes_.tolist()


def predict_output(user_input:dict):

    df = pd.DataFrame(user_input,index=[0])
    

    predicted_class = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    class_prob = dict(zip(classes_labels, map(lambda p: round(p,4), probabilities)))


    return{
        "Predicted_Category": predicted_class,
        "Confidence": round(confidence, 4),
        "Class_Probabilities":class_prob   
    }  
    