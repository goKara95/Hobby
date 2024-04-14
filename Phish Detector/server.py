from flask import Flask, render_template, request
import xgboost as xgb
import joblib
import os
import trafilatura
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load your XGBoost model
model = joblib.load('model/sbert_xgboost_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    prediction_result = "Phishing" # or it will be "Legitimate"
    if 'htmlFile' not in request.files:
        return "No file part"
    
    file = request.files['htmlFile']

    if file.filename == '':
        return "No selected file"

    # Save the uploaded file to a temporary location
    file_path = 'test/' + file.filename
    file.save(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except UnicodeError:
        with open(file_path, "r", encoding="windows-1254") as file:
            html_content = file.read()

    # START of the business logic here
    parsed_html = trafilatura.extract(html_content, include_comments=False, include_tables=False, no_fallback=True)
    # Perform prediction using the file_path with your XGBoost model
    embedding = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens').encode(parsed_html)
    embedding = embedding.reshape(1, -1)
    # Replace the following line with your actual prediction logic
    if model.predict(embedding) == 0:
        prediction_result = "Legitimate"
    # END of the business logic here
   

    return f"{file_path} is {prediction_result}"

if __name__ == '__main__':
    app.run(debug=True, port=5050)