from flask import Flask, jsonify, request
from flask_cors import CORS
from helpers import make_json
import os
import requests
from main import pdf_to_text
from HS import analyze_hs
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "data"
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/hs', methods=['POST'])
def get_hs_result():
    if request.method == 'POST':
        # Check if the request is JSON
        if request.is_json:
            # Get the JSON data
            data = request.get_json()

            # Extract HS code and description
            hs_code = data.get('hs_code')
            description = data.get('description')

            # Optionally, you can add some validation here
            if not hs_code or not description:
                return jsonify({"error": "HS code and description are required"}), 400

            # Do something with the data (e.g., print or save it)
            print(f"Received HS Code: {hs_code}")
            print(f"Received Description: {description}")

            # Return 0 as requested
            return jsonify({"result": str(analyze_hs(hs_code, description))}), 200
        else:
            return jsonify({"error": "Request must be JSON"}), 400

@app.route('/', methods=['GET','POST'])
def get_csv():

    if(request.method == 'POST'):
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        file_content = pdf_to_text(file_path)

        # Send request to ChatGPT API to extract HS code
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an assistant that extracts HS codes from documents."},
                {"role": "user", "content": f"""Extract the productname, HS code, price, and descriprion from this text. return only the mentioned elements in a dictionary
                 that has the keys:  productName , hsCode, totalPrice, and  description and nothing but that. strip it from any white space:\n\n{file_content}"""}
            ],
            "max_tokens": 100
        }


        try:
            print('here')
            response = requests.post(CHATGPT_API_URL, json=data, headers=headers)
            print('flag1')
            if response.status_code == 200:
                response_json = response.json()
                hs_code = response_json['choices'][0]['message']['content']
                print('flag2')
                return jsonify({"message": "HS code retrieved successfully", "hs_code": hs_code}), 200
            else:
                print('flag3')
                print(response.text)
                return jsonify({"error": "Failed to retrieve HS code", "details": response.text}), 500
        except Exception as e:
            print(e)
            return jsonify({"error": "Error contacting ChatGPT API", "details": str(e)}), 500
    return 'get'

