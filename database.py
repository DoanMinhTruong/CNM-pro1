import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		name TEXT,
		phone TEXT
		)''')

# conn.execute('''CREATE TABLE products
# 		(productId INTEGER PRIMARY KEY,
# 		name TEXT,
# 		price REAL,
# 		description TEXT,
# 		image TEXT,
# 		stock INTEGER,
# 		categoryId INTEGER,
# 		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
# 		)''')



conn.close()
print("CREATED DATABASE")