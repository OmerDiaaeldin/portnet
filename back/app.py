from flask import Flask, jsonify
from flask_cors import CORS
from helpers import make_json
app = Flask(__name__)
CORS(app)
@app.route('/data')
def get_csv(path = "data/Generated_Invoices.csv"):
    resp = make_json(path)
    return jsonify(resp)