from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

BASE_PATH = "./Wordlist/"
prechosen = {'a', 'd', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't'}
alphabet = set('abcdefghijklmnopqrstuvwxyz')


@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.json
    # Process your data here
    response = {"message": "Data received", "yourData": data}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
