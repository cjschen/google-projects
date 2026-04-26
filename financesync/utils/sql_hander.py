import sqlite3

con = sqlite3.connect("tutorial.db")


# Tables: 
# last_scanned
# - row: int 
# merchants
# merchant_name: str
# category: str

class SQLHander():

    def insert_merchant(merchant: str, category: str):
        cur = con.cursor()
        res = cur.execute() 

    def get_merchant_category(merchant: str) -> str:
        cur = con.cursor()
        res = cur.execute() 

    def create_tables():
        cur = con.cursor()
        query = """
                    CREATE TABLE 
                """
        res = cur.execute() 
