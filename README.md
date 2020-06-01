
# ![English](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-usa2x.png) Simple REST service in Python

This is a simple REST service that was made as a college project for the university course of Electronic and Mobile Business on the Faculty of Organization and Informatics in Varaždin, Croatia.

# Description
This REST service runs on the GCP and it's IP address is [35.242.214.64](http://35.242.214.64). The service offers data from a toned-down, MySQL version of the [Northwind database](https://docs.yugabyte.com/latest/sample-data/northwind/). Commands for creating the database were downloaded from [here](https://documentation.alphasoftware.com/pages/GettingStarted/GettingStartedTutorials/Basic%20Tutorials/Northwind/northwindMySQL.xml).

## Technologies
  - Python3 with the **Flask** web framework
  - MySQL database
  - Google Cloud Platform

## Installation

For the database, mentioned commands were used, but the database was slightly modified by changing the name of a table 'order details' to 'order_details' and by adding one more table. That table is the table 'users' for keeping the user data - usernames and SHA256 passwords. 

```sql
alter table `order details` rename order_details;
create table users (
  username varchar(20) primary key,
    password char(64) );
```

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

# Operations and examples

There are operations for every table in the database (besides the 'users' table) and every table in the database roughly has its own path(s). In the following part explains these operations.

## Categories

`GET /categories` - all categories  
`GET /categories/<filter>` - categories whose name or descriptions contains <filter> 

Examples.  
`35.242.214.64/categories`  
`35.242.214.64/categories/sweet`  

## Customers

`GET /customers` - all customers

Customers can be requested with additional query parameters. Those include: `id`, `company`, `city`, `country`.

Examples.  
`35.242.214.64/customers`  
`35.242.214.64/customers?id=queen`  
`35.242.214.64/customers?company=Cactus%20Comidas%20para%20llevar` - exact name of the company  
`35.242.214.64/customers?country=germany&city=berlin`  

## Employees

`GET /employees` - all employees

Employee requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.

Example.  
`35.242.214.64/employees`

## Order details

`GET /order_details` - all order details

Order detail requests require `username` and `password` as header parameters. The user with entered username/password must exist in the database.

Order details can be requested with additional query parameters. Those include: `order`, `product`.

Examples.  
`35.242.214.64/order_details`  
`35.242.214.64/order_details?order=10500`  
`35.242.214.64/order_details?product=39`  

## Orders

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

## Products

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

## Shippers

`GET /shippers` - all shippers  
`GET /shippers/<filter>` - shippers whose company name contains <filter>  

Examples.  
`35.242.214.64/shippers`  
`35.242.214.64/shippers/speedy`  

## Suppliers

`GET /suppliers` - all suppliers  
`POST /suppliers` - insert a new supplier  

Suppliers can be requested with additional query parameters. Those include: `id`, `company`, `city`, `country`.

Inserting a new supplier requires a **JSON body parameter** `newSupplier` and `username` and `password` as header parameters. Attributes of the `newSupplier` value are shown in a table below.

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
## Other paths and methods

If the path exists, but the method is not implemented, response consists of a message: "*The method is not allowed for the requested URL.*"

If the path doesn't exist, the response is error code *404 NOT FOUND*.

# ![Hrvatski](https://cdn3.iconfinder.com/data/icons/142-mini-country-flags-16x16px/32/flag-croatia2x.png) Jednostavni REST servis u programskom jeziku Python

Ovo je jednostavni REST servis koji je napravljen kao projekt iz kolegija Elektroničko i mobilno poslovanje na Fakultetu organizacije i informatike u Varaždinu, Hrvatskoj.

# Opis

Ovaj REST servis pokrenut je na GCP-u te mu se može pristupiti preko adrese [35.242.214.64](http://35.242.214.64). Ovaj servis nudi podatke iz nešto pojednostavljenije, MySQL verzije [Northwind baze podataka](https://docs.yugabyte.com/latest/sample-data/northwind/). Naredbe za stvaranje tablica baza podataka preuzete su s [ove poveznice](https://documentation.alphasoftware.com/pages/GettingStarted/GettingStartedTutorials/Basic%20Tutorials/Northwind/northwindMySQL.xml).

## Korištene tehnologije

  - Python3 s **Flask** okvirom
  - MySQL baza podataka
  - Google Cloud Platform

## Instalacija i pokretanje

Za stvaranje bate podataka, korištene su spomenute preuzete naredbe, no baza podataka je nešto izmijenjena. Ime tablice 'order details' promijenjeno je u 'order_details' te se stvorila jedna dodatna tablica 'users'. U toj se tablici čuvaju podaci o korisnicima - njihova korisnička imena te SHA256 sažeci lozinki.

```sql
alter table `order details` rename order_details;
create table users (
  username varchar(20) primary key,
    password char(64) );
```

U razvoju je korišten [pipenv]([https://github.com/pypa/pipenv](https://github.com/pypa/pipenv)). Popis ovisnosti može se pronaći u datoteci *Pipfile*.

Inicijaliziranje *pipenv* okoline te instalacija ovisnosti:
```sh
$ pipenv install
```
Ulazak u okolinu:
```sh
$ pipenv shell
```

Ukoliko se ne koristi *pipenv*, ovisnosti se mogu ručno instalirati pomoću *pip*-a.

Pokretanje servisa:
```sh
$ python service.py
```

# Operacije i primjeri
Postoje operacije za svaku tablicu u bazi podataka (osim za tablicu 'users') te svaka tablica ima svoju putanju na servisu. Slijedi opis dostupnih operacija.

## Kategorije

`GET /categories` - sve kategorije  
`GET /categories/<filter>` - kategorije čije ime ili opis sadrži riječ \<filter> 

Primjeri.  
`35.242.214.64/categories`  
`35.242.214.64/categories/sweet`  

## Kupci / klijenti

`GET /customers` - svi kupci

Zahtjev kupaca može sadržavati dodatne *query* parametre. Oni uključuju: `id`, `company`, `city`, `country`.

Primjeri.
`35.242.214.64/customers`  
`35.242.214.64/customers?id=queen`  
`35.242.214.64/customers?company=Cactus%20Comidas%20para%20llevar` - točno ime tvrtke  
`35.242.214.64/customers?country=germany&city=berlin`  

## Zaposlenici

`GET /employees` - svi zaposlenici

Zahtjevi za zaposlenicima zahtjevaju `username` i `password` *header* parametre. Uneseni korisnik mora postojati u bazi podataka.

Primjer.
`35.242.214.64/employees`

## Detalji narudžbi

`GET /order_details` - svi detalji narudžbi

Zahtjevi za detaljima narudžbe zahtjevaju `username` i `password` *header* parametre. Uneseni korisnik mora postojati u bazi podataka.

Zahtjev za detaljima narudžbe može sadržavati dodatne *query* parametre. Oni uključuju: `order`, `product`.

Primjeri.  
`35.242.214.64/order_details`  
`35.242.214.64/order_details?order=10500`  
`35.242.214.64/order_details?product=39`  

## Narudžbe

`GET /orders` - sve narudžbe  
`GET /orders/details` - sve narudžbe s detaljima  

Zahtjevi za narudžbama zahtjevaju `username` i `password` *header* parametre. Uneseni korisnik mora postojati u bazi podataka.

Zahtjev za narudžbama bez uključenih detalja može sadržavati dodatne *query* parametre. Oni uključuju: `id`, `customer`, `city`, `country`.

Primjeri.  
`35.242.214.64/orders`  
`35.242.214.64/orders/details`  
`35.242.214.64/orders?id=10500`  
`35.242.214.64/orders?country=brazil`  
`35.242.214.64/orders?city=berlin`  

## Proizvodi

`GET /products` - svi proizvodi

Zahtjevi za proizvodima zahtjevaju `username` i `password` *header* parametre. Uneseni korisnik mora postojati u bazi podataka.

Zahtjev za proizvodima može sadržavati dodatne **JSON body parametre**. Oni uključuju: `supplier`, `category`, `unit_price`, `units_in_stock`, `units_on_order`, `reorder_level`, `discontinued`.
Brojevni parametri moraju se definitrati pomoću  `gt` (greater than) i `lt` (less than) atributa.

Primjeri.  
`35.242.214.64/products` sa ili bez JSON tijela

Primjeri JSON tijela.
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

## Otpremnici

`GET /shippers` - svi otpremnici  
`GET /shippers/<filter>` - otpremnici čiji naziv tvrtke sadržava riječ \<filter>  

Primjeri.  
`35.242.214.64/shippers`  
`35.242.214.64/shippers/speedy`  

## Dobavljači

`GET /suppliers` - svi dobavljači  
`POST /suppliers` - unos novog dobavljača  

Zahtjev za dobavljačima može sadržavati dodatne *query* parametre. Oni uključuju: `id`, `company`, `city`, `country`.

Unos novog dobavljača zahtjeva **JSON body parametar** `newSupplier` te `username` i `password` *header* parametre. Atributi vrijednosti `newSupplier` prikazani su u tablici ispod.

| Atribut|Obavezan|
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


Primjeri. / **GET**  
`35.242.214.64/suppliers`  
`35.242.214.64/suppliers?id=20`  
`35.242.214.64/suppliers?company=ltd` - naziv tvrtke sadrži riječ 'ltd'  
`35.242.214.64/suppliers?city=manchester`  
`35.242.214.64/suppliers?country=norway`  

Primjeri. / **POST**  
`35.242.214.64/suppliers` **sa** JSON tijelom

Primjeri JSON tijela.
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
## Ostale putanje i metode

Ukoliko putanja postoji, no metoda nije implementirana, odgovor će sadržavati poruku: "*The method is not allowed for the requested URL.*"

Ukoliko tražena putanja ne postoji, odgovor će biti kod greške *404 NOT FOUND*.
