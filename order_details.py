from flask_restful import Resource, reqparse
from flask import jsonify
from connector import Connector as c
from auth import Auth


class OrderDetails(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='headers')
        parser.add_argument('password', location='headers')
        parser.add_argument('order')
        parser.add_argument('product')
        params = parser.parse_args()
        if params['username'] is None or params['password'] is None:
            response = jsonify({"error": "no username and/or password"})
            response.status_code = 400
            return response
        if Auth.check(params['username'], params['password']) == False:
            response = jsonify({"error": "user unauthorized"})
            response.status_code = 401
            return response
        query = "select * from order_details"
        query_clauses = []
        if params['order'] is not None:
            query_clauses.append(f"OrderID = '{params['order']}'")
        if params['product'] is not None:
            query_clauses.append(f"ProductID = '{params['product']}'")
        if len(query_clauses) != 0:
            query += " where " + " and ".join(query_clauses)
        c.cursor.execute(query)
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'order_details': [{'OrderID': id, 'ProductID': pid, 'UnitPrice': f"{uprice:.2f}", 'Quantity': quan, 'Discount': str(disc)} for (id, pid, uprice, quan, disc) in records]}
        return result
