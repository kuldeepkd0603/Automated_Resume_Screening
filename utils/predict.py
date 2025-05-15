import pandas as pd
import numpy as np
import joblib
from utils.preprocess import preprocess_text
from utils.constants import classification


job_role_mapping = {
    "INFORMATION-TECHNOLOGY": 0,
    "BUSINESS-DEVELOPMENT": 1,
    "ACCOUNTANT": 2,
    "ADVOCATE": 3,
    "ENGINEERING": 4,
    "CHEF": 5,
    "FITNESS": 6,
    "FINANCE": 7,
    "SALES": 8,
    "AVIATION": 9,
    "HEALTHCARE": 10,
    "CONSULTANT": 11,
    "BANKING": 12,
    "CONSTRUCTION": 13,
    "PUBLIC-RELATIONS": 14,
    "HR": 15,
    "DESIGNER": 16,
    "ARTS": 17,
    "TEACHER": 18,
    "APPAREL": 19,
    "DIGITAL-MEDIA": 20,
    "AGRICULTURE": 21,
    "AUTOMOBILE": 22,
    "BPO": 23
}
reverse_job_role_mapping = {v: k for k, v in job_role_mapping.items()}

def prediction(data):
    try:
        try:
            with open(classification.get('ml_vectorizer'),"rb") as tfidf_file:
                tfidf=joblib.load(tfidf_file)
        except Exception as e:
            return f"error occured duaring classification vectorizer loading {e}"
        
        try:
            with open(classification.get('ml_model'),"rb") as model_file:
                model=joblib.load(model_file)
        except Exception as e:
            return f"error occured duaring classification model loading {e}"
        
        try:
            with open(classification.get('label_encoder'),"rb") as vector_file:
                le=joblib.load(vector_file)
        except Exception as e:
            return f"error occured duaring classification model loading {e}"

    
        data = preprocess_text(data)
        embedded_data = tfidf.transform([data]).toarray()
        predicted_class_index = model.predict(embedded_data)[0]
    
        #predicted_job_role=le.transform(predicted_class_index)
        predicted_job_role = le.inverse_transform([predicted_class_index])[0]
        #predicted_job_role = reverse_job_role_mapping.get(int(predicted_class_index), "unknown")
        
        return predicted_job_role
    except Exception as e:
        return f"Error occurred in prediction function: {e}"