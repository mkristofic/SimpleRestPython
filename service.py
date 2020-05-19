from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="northwind",
  passwd="northwind",
  database="northwind"
)
mycursor = mydb.cursor()

app = Flask(__name__)
api = Api(app)

class Categories(Resource):
	def get(self):
		mycursor.execute("select CategoryID, CategoryName, Description from categories")
		result = {'categories': [{'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in mycursor.fetchall()]}
		return result

class CategoriesFilter(Resource):
	def get(self, filter):
		mycursor.execute("select CategoryID, CategoryName, Description from categories where CategoryName like '%{}%' or Description like '%{}%'".format(filter, filter))
		result = {'categories': [{'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in mycursor.fetchall()]}
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
			query_clauses.append("CustomerID = '{}'".format(params['id']))
		if params['company'] is not None:
			query_clauses.append("CompanyName = '{}'".format(params['company']))
		if params['city'] is not None:
			query_clauses.append("City = '{}'".format(params['city']))
		if params['country'] is not None:
			query_clauses.append("Country = '{}'".format(params['country']))
		if len(query_clauses) != 0:
			query += " where " + " and ".join(query_clauses)
		print(query)
		mycursor.execute(query)
		result = {'customers': [{'CustomerID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) in mycursor.fetchall()]}
		return result

class Shippers(Resource):
	def get(self):
		mycursor.execute("select * from shippers")
		result = {'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in mycursor.fetchall()]}
		return result

class ShippersSimilarName(Resource):
	def get(self, name):
		mycursor.execute("select * from shippers where LOWER(CompanyName) like '%{}%'".format(name.lower()))
		result = {'shippers': [{'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in mycursor.fetchall()]}
		return result

api.add_resource(Shippers, '/shippers')
api.add_resource(ShippersSimilarName, '/shippers/<name>')

if __name__ == '__main__':
	app.run(port='5002')