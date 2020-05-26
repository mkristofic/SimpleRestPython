from flask_restful import Resource, reqparse
from flask import jsonify
from connector import Connector as c
from auth import Auth


class Employees(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='headers')
        parser.add_argument('password', location='headers')
        params = parser.parse_args()
        if params['username'] is None or params['password'] is None:
            response = jsonify({"error": "no username and/or password"})
            response.status_code = 400
            return response
        if Auth.check(params['username'], params['password']) == False:
            response = jsonify({"error": "user unauthorized"})
            response.status_code = 401
            return response
        c.cursor.execute(
            "select EmployeeID, LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Notes from employees")
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'employees': [{'EmployeeID': id, 'LastName': lname, 'FirstName': fname, 'Title': title, 'TitleOfCourtesy': toc, 'BirthDate': str(bdate), 'HireDate': str(
            hdate), 'Address': address, 'City': city, 'Region': region, 'PostalCode': pcode, 'Country': country, 'HomePhone': hphone, 'Extension': extension, 'Notes': notes} for (id, lname, fname, title, toc, bdate, hdate, address, city, region, pcode, country, hphone, extension, notes) in records]}
        return result
