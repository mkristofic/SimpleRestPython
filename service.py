from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector
import hashlib
import json

mysqldb = mysql.connector.connect(
  host="localhost",
  user="northwind",
  passwd="northwind",
  database="northwind",
  auth_plugin="mysql_native_password")

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
		cursor.execute(query)
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'order_details': [{'OrderID': id, 'ProductID': pid, 'UnitPrice': f"{uprice:.2f}", 'Quantity': quan, 'Discount': str(disc)} for (id, pid, uprice, quan, disc) in records]}
		return result

class Orders(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', location='headers')
		parser.add_argument('password', location='headers')
		parser.add_argument('id')
		parser.add_argument('customer')
		parser.add_argument('city')
		parser.add_argument('country')
		params = parser.parse_args()
		if params['username'] is None or params['password'] is None:
			response = jsonify({"error": "no username and/or password"})
			response.status_code = 400
			return response
		if Auth.check(params['username'], params['password']) == False:
			response = jsonify({"error": "user unauthorized"})
			response.status_code = 401
			return response
		query = "select OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry from orders"
		query_clauses = []
		if params['id'] is not None:
			query_clauses.append(f"OrderID = '{params['id']}'")
		if params['customer'] is not None:
			query_clauses.append(f"CustomerID = '{params['customer']}'")
		if params['city'] is not None:
			query_clauses.append(f"ShipCity = '{params['city']}'")
		if params['country'] is not None:
			query_clauses.append(f"ShipCountry = '{params['country']}'")
		if len(query_clauses) != 0:
			query += " where " + " and ".join(query_clauses)
		cursor.execute(query)
		records = cursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'orders': [{'OrderID': id, 'CustomerID': customer, 'EmployeeID': employee, 'OrderDate': str(odate), 'RequiredDate': str(rdate), 'ShippedDate': str(sdate), 'ShipVia': via, 'Freight': str(freight), 'ShipName': name, 'ShippedDate': address, 'ShipCity': city, 'ShipRegion': region, 'ShipPostalCode': postal, 'ShipCountry': country} for (id, customer, employee, odate, rdate, sdate, via, freight, name, address, city, region, postal, country) in records]}
		return result

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

		cursor.execute(query)
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
			response = jsonify({"error": "no required companyName attribute found"})
			response.status_code = 400
			return response

		columns = [ 'CompanyName' ]
		values = [ supplier['companyName'] ]

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
		query = "insert into suppliers (" + ', '.join(columns) + ") VALUES (\"" + '", "'.join(values) + "\")"
		cursor.execute(query)
		mysqldb.commit()
		rows = cursor.rowcount
		if rows == 1:
			response = jsonify({"ok": "supplier successfully inserted"})
			response.status_code = 200
			return response
		else:
			response = jsonify({"error": "supplier not inserted"})
			response.status_code = 400
			return response

class Reject(Resource):
	def put(self):
		response = jsonify({"error": "not supported"})
		response.status_code = 405
		return response

	def delete(self):
		response = jsonify({"error": "not supported"})
		response.status_code = 405
		return response

api.add_resource(Categories, '/categories')
api.add_resource(Customers, '/customers')
api.add_resource(Employees, '/employees')
api.add_resource(CategoriesFilter, '/categories/<filter>')
api.add_resource(OrderDetails, '/order_details')
api.add_resource(Orders, '/orders')
api.add_resource(Products, '/products')
api.add_resource(Shippers, '/shippers')
api.add_resource(ShippersFilter, '/shippers/<filter>')
api.add_resource(Suppliers, '/suppliers')
api.add_resource(Reject, '/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='80')