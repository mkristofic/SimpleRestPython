from flask import jsonify
from flask_restful import Resource

class Reject(Resource):
    def put(self):
        response = jsonify({"error": "not supported"})
        response.status_code = 405
        return response

    def delete(self):
        response = jsonify({"error": "not supported"})
        response.status_code = 405
        return response