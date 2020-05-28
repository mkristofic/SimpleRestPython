from flask_restful import Resource, reqparse
from flask import jsonify
from connector import Connector as c
from auth import Auth


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
        c.cursor.execute(query)
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'orders': [{'OrderID': id, 'CustomerID': customer, 'EmployeeID': employee, 'OrderDate': str(odate), 'RequiredDate': str(rdate), 'ShippedDate': str(sdate), 'ShipVia': via, 'Freight': str(freight), 'ShipName': name, 'ShippedDate': address, 'ShipCity': city, 'ShipRegion': region, 'ShipPostalCode': postal, 'ShipCountry': country} for (id, customer, employee, odate, rdate, sdate, via, freight, name, address, city, region, postal, country) in records]}
        return result

class OrdersAndDetails(Resource):
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
        query = "select o.OrderID, o.CustomerID, o.EmployeeID, o.OrderDate, o.RequiredDate, o.ShippedDate, o.ShipVia, o.Freight, o.ShipName, o.ShipAddress, o.ShipCity, o.ShipRegion, o.ShipPostalCode, o.ShipCountry, od.*, p.*, c.CategoryName, c.Description from orders o join order_details od on o.OrderID = od.OrderID join products p on od.ProductID = p.ProductID join categories c on c.CategoryID = p.CategoryID order by o.OrderID"
        c.cursor.execute(query)
        records = c.cursor.fetchall()
        previous_oid = 0
        orders_array = []
        details_array = []
        for (id, customer, employee, odate, rdate, sdate, via, freight, name, address, city, region, postal, country, oid, opid, ounit, oquan, odisc, pid, pname, psid, pcid, pquan, punit, pstock, porder, preorder, pdisc, cname, cdesc) in records:
            
            if previous_oid != id and previous_oid != 0:
                one_order = {'OrderID': id, 'CustomerID': customer, 'EmployeeID': employee, 'OrderDate': str(odate), 'RequiredDate': str(rdate), 'ShippedDate': str(sdate), 'ShipVia': via, 'Freight': str(freight), 'ShipName': name, 'ShippedDate': address, 'ShipCity': city, 'ShipRegion': region, 'ShipPostalCode': postal, 'ShipCountry': country, 'OrderDetails': details_array}
                details_array = []
                orders_array.append(one_order)

            category = {'CategoryName': cname, 'Description': cdesc}
            product = {'ProductID': pid, 'ProductName': pname, 'SupplierID': psid, 'Category': category, 'QuantityPerUnit': pquan, 'UnitPrice': f"{punit:.2f}", 'UnitsInStock': pstock, 'UnitsOnOrder': porder, 'ReorderLevel': preorder, 'Discontinued': pdisc == 1}
            one_detail = {'Product': product, 'UnitPrice': f"{ounit:.2f}", 'Quantity': oquan, 'Discount': str(odisc)}
            details_array.append(one_detail)
            previous_oid = id

        result = {"orders": orders_array}
        return result



