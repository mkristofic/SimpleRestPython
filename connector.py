import mysql.connector


class Connector:

    mysqldb = mysql.connector.connect(
        host="localhost",
        user="northwind",
        passwd="northwind",
        database="northwind",
        auth_plugin="mysql_native_password")

    cursor = mysqldb.cursor()
