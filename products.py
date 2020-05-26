from flask_restful import Resource, reqparse
from flask import jsonify
from connector import Connector as c
from auth import Auth
import json


class Products(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='headers')
        parser.add_argument('password', location='headers')
        parser.add_argument('supplier', location='json')
        parser.add_argument('category', location='json')
        parser.add_argument('unit_price', location='json')
        parser.add_argument('units_in_stock', location='json')
        parser.add_argument('units_on_order', location='json')
        parser.add_argument('reorder_level', location='json')
        parser.add_argument('discontinued', location='json')
        params = parser.parse_args()

        if params['username'] is None or params['password'] is None:
            response = jsonify({"error": "no username and/or password"})
            response.status_code = 400
            return response
        if Auth.check(params['username'], params['password']) == False:
            response = jsonify({"error": "user unauthorized"})
            response.status_code = 401
            return response

        query = "select * from products"
        query_clauses = []
        unit_price = params['unit_price']
        units_in_stock = params['units_in_stock']
        units_on_order = params['units_on_order']
        reorder_level = params['reorder_level']
        if unit_price is not None:
            unit_price = json.loads(unit_price.replace('\'', '"'))
            if unit_price['gt'] is not None:
                query_clauses.append(f"UnitPrice > {unit_price['gt']}")
            if unit_price['lt'] is not None:
                query_clauses.append(f"UnitPrice < {unit_price['lt']}")
        if units_in_stock is not None:
            units_in_stock = json.loads(units_in_stock.replace('\'', '"'))
            if 'gt' in units_in_stock:
                query_clauses.append(f"UnitsInStock > {units_in_stock['gt']}")
            if 'lt' in units_in_stock:
                query_clauses.append(f"UnitsInStock < {units_in_stock['lt']}")
        if units_on_order is not None:
            units_on_order = json.loads(units_on_order.replace('\'', '"'))
            if 'gt' in units_on_order:
                query_clauses.append(f"UnitsOnOrder > {units_on_order['gt']}")
            if 'lt' in units_on_order:
                query_clauses.append(f"UnitsOnOrder < {units_on_order['lt']}")
        if reorder_level is not None:
            reorder_level = json.loads(reorder_level.replace('\'', '"'))
            if 'gt' in reorder_level:
                query_clauses.append(f"ReorderLevel > {reorder_level['gt']}")
            if 'lt' in reorder_level:
                query_clauses.append(f"ReorderLevel < {reorder_level['lt']}")
        if params['supplier'] is not None:
            query_clauses.append(f"SupplierID = {params['supplier']}")
        if params['category'] is not None:
            query_clauses.append(f"CategoryID = {params['category']}")
        if params['category'] is not None:
            query_clauses.append(f"CategoryID = {params['category']}")
        if params['discontinued'] is not None:
            query_clauses.append(f"Discontinued = {params['discontinued']}")

        if len(query_clauses) != 0:
            query += " where " + " and ".join(query_clauses)

        c.cursor.execute(query)
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'products': [{'ProductID': id, 'ProductName': name, 'SupplierID': supplier, 'CategoryID': category, 'QuantityPerUnit': quan, 'UnitPrice': f"{uprice:.2f}", 'UnitsInStock': stock, 'UnitsOnOrder': order, 'ReorderLevel': reorder, 'Discontinued': disc == 1} for (id, name, supplier, category, quan, uprice, stock, order, reorder, disc) in records]}
        return result
