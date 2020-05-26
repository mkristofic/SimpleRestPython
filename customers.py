from flask_restful import Resource, reqparse
from connector import Connector as c


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
        c.cursor.execute(query)
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'customers': [{'CustomerID': id, 'CompanyName': company, 'ContactName': contact_name, 'ContactTitle': contact_title, 'Address': address, 'City': city, 'Region': region, 'PostalCode': postal_code, 'Country': country, 'Phone': phone, 'Fax': fax} for (id, company, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) in records]}
        return result
