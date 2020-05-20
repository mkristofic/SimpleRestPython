from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector
import hashlib

mysqldb = mysql.connector.connect(
  host="localhost",
  user="northwind",
  passwd="northwind",
  database="northwind"
)
cursor = mysqldb.cursor()



app = Flask(__name__)
api = Api(app)

class Auth:
	@staticmethod
	def check(username, password):
		pass_hash = hashlib.sha256(str.encode(password)).hexdigest()
		cursor.execute(f"select * from users where username = '{username}' and password = '{pass_hash}'")
		records = cursor.fetchall()
		return len(records) == 1

class Categories(Resource):
	def get(self):
		cursor.execute("select CategoryID, CategoryName, Description from categories")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'categories': [{'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in records]}
		return result

class CategoriesFilter(Resource):
	def get(self, filter):
		cursor.execute(f"select CategoryID, CategoryName, Description from categories where CategoryName like '%{filter}%' or Description like '%{filter}%'")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'categories': [{'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in records]}
		return result

class Customers(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id')
		parser.add_argument('company')
		parser.add_argument('city')
		parser.add_argument('country')
		params = parser.parse_args()
		query = "select CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax from customers"
		query_clauses = []
		if params['id'] is not None:
			query_clauses.append(f"CustomerID = '{params['id']}'")
		if params['company'] is not None:
			query_clauses.append(f"CompanyName = '{params['company']}'")
		if params['city'] is not None:
			query_clauses.append(f"City = '{params['city']}'")
		if params['country'] is not None:
			query_clauses.append(f"Country = '{params['country']}'")
		if len(query_clauses) != 0:
			query += " where " + " and ".join(query_clauses)
		cursor.execute(query)
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'customers': [{'CustomerID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) in records]}
		return result

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
		cursor.execute("select EmployeeID, LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Notes from employees")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'employees': [{'EmployeeID': id, 'LastName': lname, 'FirstName': fname, 'Title': title, 'TitleOfCourtesy': toc, 'BirthDate': str(bdate), 'HireDate': str(hdate), 'Address': address, 'City': city, 'Region': region, 'PostalCode': pcode, 'Country': country, 'HomePhone': hphone, 'Extension': extension, 'Notes': notes} for (id, lname, fname, title, toc, bdate, hdate, address, city, region, pcode, country, hphone, extension, notes) in records]}
		return result

class Products(Resource):
	def get(self):
		cursor.execute("select * from products")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'products': [{'ProductID': id, 'ProductName': name, 'SupplierID': supplier, 'CategoryID': category, 'QuantityPerUnit': quan, 'UnitPrice': f"{uprice:.2f}", 'UnitsInStock': stock, 'UnitsOnOrder': order, 'ReorderLevel': reorder, 'Discontinued': disc == 1} for (id, name, supplier, category, quan, uprice, stock, order, reorder, disc) in records]}
		return result

class Shippers(Resource):
	def get(self):
		cursor.execute("select * from shippers")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
		return result

class ShippersFilter(Resource):
	def get(self, filter):
		cursor.execute(f"select * from shippers where LOWER(CompanyName) like '%{filter.lower()}%'")
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
		return result

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
			query_clauses.append(f"CompanyName = '{params['company']}'")
		if params['city'] is not None:
			query_clauses.append(f"City = '{params['city']}'")
		if params['country'] is not None:
			query_clauses.append(f"Country = '{params['country']}'")
		if len(query_clauses) != 0:
			query += " where " + " and ".join(query_clauses)
		cursor.execute(query)
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'suppliers': [{'SupplierID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax, 'HomePage': homepage} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax, homepage) in records]}
		return result

api.add_resource(Categories, '/categories')
api.add_resource(Customers, '/customers')
api.add_resource(Employees, '/employees')
api.add_resource(CategoriesFilter, '/categories/<filter>')
api.add_resource(Products, '/products')
api.add_resource(Shippers, '/shippers')
api.add_resource(ShippersFilter, '/shippers/<filter>')
api.add_resource(Suppliers, '/suppliers')

if __name__ == '__main__':
	app.run(host='localhost', port='5002')