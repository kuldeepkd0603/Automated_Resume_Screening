import pandas as pd
import numpy as np
import joblib
from utils.preprocess import preprocess_text
import pickle
from utils.constants import clustering





def cluster(data):
    try:
        try:
            with open(clustering.get('vectorizer'),'rb') as tfidf_file:
                tfidf=joblib.load(tfidf_file)
        except Exception as e:
            return f"error occured during loading of clustering vectorizer {e}"
        try:
            with open(clustering.get('kmeans_model'),'rb') as kmean_model_file:
                kmeans_model=joblib.load(kmean_model_file)
        except Exception as e:
            return f"error occured during loading of clustering model {e}"
        
        try:
            with open(clustering.get('pca'), 'rb') as pca_file:
                pca = joblib.load(pca_file)
        except Exception as e:
            return f"error occured during loading of clustering pca model {e}"  
         

        data = preprocess_text(data)
        vectorized_text = tfidf.transform([data]).toarray()
        reduced_text = pca.transform(vectorized_text)
      
        cluster_label = kmeans_model.predict(reduced_text)[0]

        
        return int(cluster_label)
    except Exception as e:
        return f"Error occurred in prediction function: {e}"