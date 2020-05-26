from flask_restful import Resource
from connector import Connector as c


class Shippers(Resource):
    def get(self):
        c.cursor.execute("select * from shippers")
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'shippers': [
            {'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
        return result


class ShippersFilter(Resource):
    def get(self, filter):
        c.cursor.execute(f"select * from shippers where LOWER(CompanyName) like '%{filter.lower()}%'")
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'shippers': [
            {'ShipperID': id, 'CompanyName': company, 'Phone': phone} for (id, company, phone) in records]}
        return result
