from flask import Flask,render_template,request
import os
import joblib
import docx2txt
import PyPDF2
from utils.ner import extract_resume_info,save_to_csv
from utils.text_extracter import extract_text
from utils.predict import prediction
from utils.clustering import cluster

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/classify',methods=['POST'])
def classify_resume():
    try:
        
        resume_text = ''
        
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file.filename != '':
                file_path = os.path.join('uploads', file.filename)
                file.save(file_path)
                resume_text = extract_text(file_path)
    
        if 'resume_text' in request.form:
            resume_text += request.form['resume_text']
        
        model_prediction= prediction(resume_text)
        cluster_prediction=cluster(resume_text)
        resume_info=extract_resume_info(resume_text,model_prediction)
        save_to_csv(resume_text,model_prediction)
        return render_template('result.html', model_prediction=model_prediction,cluster_prediction=cluster_prediction ,resumeInfo=resume_info)
    except Exception as e:
        return f"error occured in main   resume function {e}"
if __name__ =='__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
