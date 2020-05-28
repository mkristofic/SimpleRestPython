from flask import Flask
from flask_restful import Api

from categories import Categories, CategoriesFilter
from customers import Customers
from employees import Employees
from order_details import OrderDetails
from orders import Orders, OrdersAndDetails
from products import Products
from shippers import Shippers, ShippersFilter
from suppliers import Suppliers

app = Flask(__name__)
api = Api(app)

api.add_resource(Categories, '/categories')
api.add_resource(CategoriesFilter, '/categories/<filter>')
api.add_resource(Customers, '/customers')
api.add_resource(Employees, '/employees')
api.add_resource(OrderDetails, '/order_details')
api.add_resource(Orders, '/orders')
api.add_resource(OrdersAndDetails, '/orders/details')
api.add_resource(Products, '/products')
api.add_resource(Shippers, '/shippers')
api.add_resource(ShippersFilter, '/shippers/<filter>')
api.add_resource(Suppliers, '/suppliers')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')