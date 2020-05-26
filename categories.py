from flask_restful import Resource
from connector import Connector as c


class Categories(Resource):
    def get(self):
        c.cursor.execute(
            "select CategoryID, CategoryName, Description from categories")
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'categories': [
            {'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in records]}
        return result


class CategoriesFilter(Resource):
    def get(self, filter):
        c.cursor.execute(f"select CategoryID, CategoryName, Description from categories where CategoryName like '%{filter}%' or Description like '%{filter}%'")
        records = c.cursor.fetchall()
        rows = len(records)
        result = {'count': rows, 'categories': [
            {'CategoryID': id, 'CategoryName': name, 'Description': desc} for (id, name, desc) in records]}
        return result
