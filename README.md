
# ![English](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-usa2x.png) Simple REST service in Python

This is a simple REST service was made as a college project for the university course of Electronic and Mobile Business on the Faculty of Organization and Informatics in Varaždin, Croatia.

# Description
This REST service runs on the GCP and it's IP address is [35.242.214.64](http://35.242.214.64). The service offers data from a toned-down MySQL version of the [Northwind database](https://docs.yugabyte.com/latest/sample-data/northwind/). Commands for creating the database were downloaded from [here](https://documentation.alphasoftware.com/pages/GettingStarted/GettingStartedTutorials/Basic%20Tutorials/Northwind/northwindMySQL.xml).

## Technologies
  - Python3 with the **Flask** web framework
  - MySQL database
  - Google Cloud Platform

## Installation

Python's [pipenv]([https://github.com/pypa/pipenv](https://github.com/pypa/pipenv)) was used. List of dependencies can be found in the *Pipfile*.

Initialize the environment and install the dependencies with:
```sh
$ pipenv install
```
Enter the environment with:
```sh
$ pipenv shell
```

If not using *pipenv*, dependencies can be manually installed via *pip*.

Run the service with:
```sh
$ python service.py
```

## Operations and examples

There are operations for every table in the database and every table in the database roughly has its own path(s). In the following part explains these operations.

### Categories

`GET /categories` - all categories  
`GET /categories/<filter>` - categories whose name or descriptions contains <filter> 

Examples.  
`35.242.214.64/categories`  
`35.242.214.64/categories/sweet`  

### Customers

`GET /customers` - all customers

Customers can be requested with additional query parameters. Those include: `id`, `company`, `city`, `country`.

Examples.  
`35.242.214.64/customers`  
`35.242.214.64/customers?id=queen`  
`35.242.214.64/customers?company=Cactus%20Comidas%20para%20llevar` - exact name of the company  
`35.242.214.64/customers?country=germany&city=berlin`  

### Employees

`GET /employees` - all employees

Employee requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.

Example.  
`35.242.214.64/employees`

### Order details

`GET /order_details` - all order details

Order detail requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.
Order details can be requested with additional query parameters. Those include: `order`, `product`.

Examples.  
`35.242.214.64/order_details`  
`35.242.214.64/order_details?order=10500`  
`35.242.214.64/order_details?product=39`  

### Orders

`GET /orders` - all orders  
`GET /orders/details` - all orders with details embedded  

Order requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.
Orders without details can be requested with additional query parameters. Those include: `id`, `customer`, `city`, `country`.

Examples.  
`35.242.214.64/orders`  
`35.242.214.64/orders/details`  
`35.242.214.64/orders?id=10500`  
`35.242.214.64/orders?country=brazil`  
`35.242.214.64/orders?city=berlin`  

### Products

`GET /products` - all products

Product requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.

Products can be requested with aditional **JSON body parameters**. Those include: `supplier`, `category`, `unit_price`, `units_in_stock`, `units_on_order`, `reorder_level`, `discontinued`.
Numeric parameters must be defined by using `gt` (greater than) and `lt` (less than) attributes.

Examples.  
`35.242.214.64/products` with or without the JSON body

Body examples.
```json
{
  "product": 5,
  "supplier": 3
}
```
```json
{
  "unit_price": {
    "gt": 10,
    "lt": 20
  }
}
```
```json
{
  "unit_price": {
    "gt": 10
  },
  "units_in_stock" : {
    "gt": 10,
    "lt": 15
  },
  "units_on_order":{
    "lt": 25
  }
}
```
```json
{
  "supplier": 1,
  "reorder_level": {
    "gt": 0
  },
  "discontinued": false
}
```
```json
{
  "discontinued": true
}
```

### Shippers

`GET /shippers` - all shippers  
`GET /shippers/<filter>` - shippers whose company name contains <filter>  

Examples.  
`35.242.214.64/shippers`  
`35.242.214.64/shippers/speedy`  

### Suppliers

`GET /suppliers` - all shippers  
`POST /suppliers` - insert a new shipper  

Suppliers can be requested with additional query parameters. Those include: `id`, `company`, `city`, `country`.

Inserting a new supplier requires a **JSON body parameter** `newSupplier`. Attributes of the `newSupplier` value are shown in a table below.

| Attribute|Required|
|----------:|:-------------:|
| companyName | :heavy_check_mark: |
| contactName || 
| contactTitle ||
| address ||
| city ||
| region ||
| postalCode ||
| country ||
| phone ||
| fax ||
| homePage ||


Examples. / **GET**  
`35.242.214.64/suppliers`  
`35.242.214.64/suppliers?id=20`  
`35.242.214.64/suppliers?company=ltd` - company contains 'ltd'  
`35.242.214.64/suppliers?city=manchester`  
`35.242.214.64/suppliers?country=norway`  

Example. / **POST**  
`35.242.214.64/suppliers` **with** the JSON body

Body examples.
```json
{
  "newSupplier": {
    "companyName": "New Company Ltd."
  }
}
```
```json
{
  "newSupplier": {
    "companyName": "Another New Company Ltd.",
    "contactName": "Leslie Miller",
    "city": "Wellington",
    "country": "New Zealand"
  }
}
```
```json
{
  "newSupplier": {
    "companyName": "Yet Another New Company Ltd.",
    "contactName": "Jude Walsh",
    "contactTitle": "Sales Representative",
    "address": "60 Marcus Clarke St, Canberra, ACT 2601",
    "city": "Canberra",
    "region": "New South Wales",
    "postalCode": "2601",
    "country": "Australia",
    "phone": "(02) 6101 7422",
    "fax": "(02) 6101 7433",
    "homePage": "yancltd.com"
  }
}
```
### Other paths and methods

If the path exists, but the method is not implemented, response consists of a message: "*The method is not allowed for the requested URL.*"

If the path doesn't exist, the response is error code *404 NOT FOUND*.

# ![Hrvatski](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-croatia2x.png) Jedostavni REST servis u programskom jeziku Python