from flask import Flask, make_response, jsonify, request

app = Flask(__name__)

@app.route('/test.json')
def json():
    return_data = {"res": "success"}
    json_data = jsonify(return_data)

    resp = make_response(json_data)
    resp.headers['Access-Control-Allow-Origin']='*'
    
    return resp


