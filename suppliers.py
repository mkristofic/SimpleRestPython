from flask_restful import Resource, reqparse
from flask import jsonify
from connector import Connector as c
from auth import Auth
import json


class Suppliers(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('company')
        parser.add_argument('city')
        parser.add_argument('country')
        params = parser.parse_args()
        query = "select SupplierID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax, HomePage from suppliers"
        query_clauses = []
        if params['id'] is not None:
            query_clauses.append(f"SupplierID = '{params['id']}'")
        if params['company'] is not None:
            query_clauses.append(f"CompanyName LIKE '%{params['company']}%'")
        if params['city'] is not None:
            query_clauses.append(f"City = '{params['city']}'")
        if params['country'] is not None:
            query_clauses.append(f"Country = '{params['country']}'")
        if len(query_clauses) != 0:
            query += " where " + " and ".join(query_clauses)
        c.cursor.execute(query)
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'suppliers': [{'SupplierID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax, 'HomePage': homepage} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax, homepage) in records]}
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='headers')
        parser.add_argument('password', location='headers')
        parser.add_argument('newSupplier', location='json')
        params = parser.parse_args()

        if params['username'] is None or params['password'] is None:
            response = jsonify({"error": "no username and/or password"})
            response.status_code = 400
            return response
        if Auth.check(params['username'], params['password']) == False:
            response = jsonify({"error": "user unauthorized"})
            response.status_code = 401
            return response

        if params['newSupplier'] is None:
            response = jsonify({"error": "no newSupplier attribute found"})
            response.status_code = 400
            return response

        supplier = json.loads(params['newSupplier'].replace('\'', '"'))
        if 'companyName' not in supplier:
            response = jsonify(
                {"error": "no required companyName attribute found"})
            response.status_code = 400
            return response

        columns = ['CompanyName']
        values = [supplier['companyName']]

        if 'contactName' in supplier:
            columns.append('ContactName')
            values.append(supplier['contactName'])
        if 'contactTitle' in supplier:
            columns.append('ContactTitle')
            values.append(supplier['contactTitle'])
        if 'address' in supplier:
            columns.append('Address')
            values.append(supplier['address'])
        if 'city' in supplier:
            columns.append('City')
            values.append(supplier['city'])
        if 'region' in supplier:
            columns.append('Region')
            values.append(supplier['region'])
        if 'postalCode' in supplier:
            columns.append('PostalCode')
            values.append(supplier['postalCode'])
        if 'country' in supplier:
            columns.append('Country')
            values.append(supplier['country'])
        if 'phone' in supplier:
            columns.append('Phone')
            values.append(supplier['phone'])
        if 'fax' in supplier:
            columns.append('Fax')
            values.append(supplier['fax'])
        if 'homePage' in supplier:
            columns.append('HomePage')
            values.append(supplier['homePage'])
        query = "insert into suppliers (" + ', '.join(columns) + \
            ") VALUES (\"" + '", "'.join(values) + "\")"
        c.cursor.execute(query)
        rows = c.cursor.rowcount
        if rows == 1:
            response = jsonify({"ok": "supplier successfully inserted"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"error": "supplier not inserted"})
            response.status_code = 400
            return response
