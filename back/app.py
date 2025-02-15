from flask import Flask, jsonify
from helpers import make_json
app = Flask(__name__)

@app.route('/data')
def get_csv(path = "data/Generated_Invoices.csv"):
    resp = make_json(path)
    return jsonify(resp)