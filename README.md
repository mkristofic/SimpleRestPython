# ![English](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-croatia2x.png) Simple REST service in Python

This is a simple REST service was made as a college project for the university course of Electronic and Mobile Business on the Faculty of Organization and Informatics in Varaždin, Croatia.

# Description
This REST service runs on the GCP and it's IP address is [35.242.214.64](http://35.242.214.64). The service offers data from a toned-down MySQL version of the [Northwind database](https://docs.yugabyte.com/latest/sample-data/northwind/). Commands for creating the database were downloaded from [here](https://documentation.alphasoftware.com/pages/GettingStarted/GettingStartedTutorials/Basic%20Tutorials/Northwind/northwindMySQL.xml).

## Technologies
  - Python3 with the **Flask** web framework
  - MySQL database
  - Google Cloud Platform

## Installation

## Operations and examples

There are operations for every table in the database and every table in the database roughly has its own path(s). In the following part explains these operations.

### Categories

`/categories` - all categories
`/categories/<filter>` - categories whose name or descriptions contains <filter>

Examples.
`35.242.214.64/categories`
`35.242.214.64/categories/sweet`

### Customers

`/customers` - all customers

Customers can be requested with additional query parameters. Those include: `id`, `company`, `city`, `country`.

Examples.
`35.242.214.64/customers`
`35.242.214.64/customers?id=queen`
`35.242.214.64/customers?company=Cactus%20Comidas%20para%20llevar`
`35.242.214.64/customers?country=germany&city=berlin`

### Employees

`/employees` - all employees

Employees requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.

Example.
`35.242.214.64/employees`

### Order details

`/order_details` - all order details

Order details requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.
Order details can be requested with additional query parameters. Those include: `order`, `product`.

Examples.
`35.242.214.64/order_details`
`35.242.214.64/order_details?order=10500`
`35.242.214.64/order_details?product=39`

### Orders

`/orders` - all orders
`/orders/details` - all orders with details embedded

Order requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.
Orders without details can be requested with additional query parameters. Those include: `id`, `customer`, `city`, `country`.

Examples.
`35.242.214.64/orders`
`35.242.214.64/orders/details`
`35.242.214.64/orders?id=10500`
`35.242.214.64/orders?country=brazil`
`35.242.214.64/orders?city=berlin`

# ![Hrvatski](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-croatia2x.png) Jedostavni REST servis u programskom jeziku Python