import sqlite3
c = sqlite3.connect('C:\\Hacking-Tolls\\Injection-Test\\backend\\secureshop.db')
print(c.execute("SELECT * FROM products WHERE name LIKE '%' UNION SELECT 1,2,3,4,5 --%'").fetchall())
