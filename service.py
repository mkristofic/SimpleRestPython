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