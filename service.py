from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector
import hashlib

mydb = mysql.connector.connect(
  host="localhost",
  user="northwind",
  passwd="northwind",
  database="northwind"
)
mycursor = mydb.cursor()

app = Flask(__name__)
api = Api(app)

class Auth():
	def check(username, password):
		pass_hash = hashlib.sha256(str.encode(password)).hexdigest()
		mycursor.execute(f"select * from users where username = '{username}' and password = '{pass_hash}'")
		records = mycursor.fetchall()
		return len(records) == 1

class Categories(Resource):
	def get(self):
		mycursor.execute("select CategoryID, CategoryName, Description from categories")
		records = mycursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'categories': [{'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in records]}
		return result

class CategoriesFilter(Resource):
	def get(self, filter):
		mycursor.execute(f"select CategoryID, CategoryName, Description from categories where CategoryName like '%{filter}%' or Description like '%{filter}%'")
		records = mycursor.fetchall()
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
		print(query)
		mycursor.execute(query)
		records = mycursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'customers': [{'CustomerID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) in records]}
		return result

class Shippers(Resource):
	def get(self):
		mycursor.execute("select * from shippers")
		records = mycursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
		return result

class ShippersFilter(Resource):
	def get(self, filter):
		mycursor.execute(f"select * from shippers where LOWER(CompanyName) like '%{filter.lower()}%'")
		records = mycursor.fetchall()
		rows = len(records)
		result = {'count': rows, 'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
		return result

api.add_resource(Customers, '/customers')
api.add_resource(Categories, '/categories')
api.add_resource(CategoriesFilter, '/categories/<filter>')
api.add_resource(Shippers, '/shippers')
api.add_resource(ShippersFilter, '/shippers/<filter>')

if __name__ == '__main__':
	app.run(host='localhost', port='5002')