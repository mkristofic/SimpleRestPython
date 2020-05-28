# ![English](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAWCAYAAAChWZ5EAAACpUlEQVRIS6VWMWsUQRT+5nZvN5AEEU1iET0C/oAFT7jSP2ARYop4pruIIFYWFiIu2ihyRYh23lok1yk2KijYWR0W9w/ShGBAe+O5N/Jm85bZuZndI06zN7sz733fm+99c+LuucubHy6uJb/q533Q8GrqgXScPSvmwqtBzAR4+O2eWi4BiGxnYZjvJXAEiS3RiB6MfoqzWfKKYQmikomwjkff71dttwE6EnNXX8jx3xRfko6CvhkP1cLdxxGEAG7FQ8VqT5vTd5rTevruBT4GvZYTAIGkGPp4mfQz8ARAEoA3HfWifQJgL44q53RYNwlA3ccgsQOwJScgBICGmG91ZXo8wlKjmTPnSlQxZ0b12RCfBhs5QT2pC8C7/YMMwFyrK+XxCAuNpmJcxXw3jkDMuVIUJJgN8VEDwEhMIPSej4IAKE3xEXxOOtYzp0QUiDVhzqfRgE0cpRogZP0SDZjf/RMNmEIzE3NF6LmTi7DVlWNDA6x+vRuYua5+lwb0xOwJDI5BTGhgsdFUZ+JiTmq3aYT2hA4NmED0Cr3dPzDaMOlAGj5g+oLLJ3QfsHWAWYViG7IRaT7AleA+V8ajaUK1ZxzBA7ARD8EaUG1l2LFZeq5K7gPchnQEpx1lPmCLSSDpCBTgM9d2ZPr7Dy5cuqKatBZ4ikU6Sq1zLyDexe/h/Azef10t5HIZEC/KfeDJdk+GYYCt9vppCzDhgFXJCxp4ut2TgQagbHNVYP38dcXb9r1K+pkTPvczd1xbWS6twP8AsxkSaaAA4MbK8sSVWcVYV72r5133Qe4DLg3YetelaP6j4mo583IqWDEBIA3cbq/nPWy7zVxsbcxdXqDH0DXwA8CSjZ3r/51LLNOu1yp2KJ55uC4EXgNYnCawnsT1e8p+PpQSd/4B4TBr8ysqdboAAAAASUVORK5CYII=) Simple REST service in Python

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

# ![Hrvatski](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAYCAYAAACbU/80AAADcUlEQVRIS61WXUhUQRT+xnbv3dUoia3cZRN8iAxC0XKDjMywCPLBHgIjggyi0ALFIAghKOvN1AdhI3qoEKSEfBCCktSih6IMyyjECtPEIqjEn/2ziTO7c7te788Gzcu9Z37OfOf7zpkZ9iE3sPPLt++PItGYG4bGAHBj53+yPaqSWL/OV84GPUo8Go25nPw6gXEaJ//GOV5FibMHDJwG8oNBDQNFTX36ZtZnB9pp/rvJSbGHKQAnNtIdl/LJYPSgCIBghRign83BoPhxitwpMvJlNUf20/e9GQC7yPrzQlhwe5A5PooIc0H1BzDv9iBrfBQLzAWPP6CNk70/kqTYqhEAASjdHMht7BO+lM6wWBg/ckqz6SeWst2dYbHx2HS3LRMEQOTAQwZODq0kkBFIAHID2pDWqZ1hMUUCIIDUCIBZkzJoDFxsv8FVRUFdTbVWJmZJw/eGhD9vwgvOOaIDj4WtlpeBcY5Iypbz2MPntlXVcu1WkgEJ4HRNtSVlwlPVHmBuFh5lDTA7h8jgE9Ht2b0LxKGw52bBaV7WSrCeR7bFQgBEFRAARVFwpqbadgE/WgVMTwG3e8ByAvCUlyU3TkVO9u+1PsR+TIDnBMBu9yzxZ6wMDcClFABiQDZ9uWhyNDUAz56CNbcC20uh7t6VpF7HRGLzRsTH3gChUrDLrbaMLmGAckAPwJSKrpvgNzqQUbAN6suRJZHLnKBxdN0EO14LHD5mySgFeFVKYMaAcaVg5O0wUH8C3LcO3ukZRPpTSSiZGBgEycS+ToO3XgfbUijcWB1KljmgX6CXQnhrPAm8fgVWdxZqe8eS7M9oqMXiyAugoAis5Zqt/jT47xLQqsE+8ObzYC43MvIL4R79iOidbqDvPni4DUjEwZqugJdVWB7p8n7QJFBL6kVfbnHlMtSiTHS9NPHC1F0c/Pm3xvWL7mWHcDFwaJn2ZjJ8HupNlqFSUi+u4w3FldpmZlWg97pvZhgHfg6haOGTkOFVZh56s7fiwaqk7sZqMstGDYAVA1YpbIzGLmfkA8TsOy4ZkAAkA05XqVmETle0rQT/yoDdcWl6gFm8MSaMDBiT0KqG7aJN50EjAyAJxGWUtePcVCIe9dsdGnZRmyWckyRyjculTjLf/rZN87+mBhYTsZx0NkonOWWt2z3vVrjUyczV/oo/hiCJyHL2TtYAAAAASUVORK5CYII=) Jedostavni REST servis u programskom jeziku Python