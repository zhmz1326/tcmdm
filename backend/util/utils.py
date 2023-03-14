from flask import jsonify

def error(code, msg):
    json_dict = {
        "code": code,
        "msg": msg
    }
    return jsonify(json_dict)

def success(data):
    json_dict = {
        "code": 200,
        "data": data
    }
    return jsonify(json_dict)