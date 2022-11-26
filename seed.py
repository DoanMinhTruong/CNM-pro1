import sqlite3

conn = sqlite3.connect('database.db')

# conn.execute('''CREATE TABLE users 
# 		(userId INTEGER PRIMARY KEY, 
# 		password TEXT,
# 		email TEXT,
# 		name TEXT,
# 		phone TEXT
# 		)''')

# conn.execute('''CREATE TABLE products
# 		(productId INTEGER PRIMARY KEY,
# 		name TEXT,
# 		price REAL,
# 		description TEXT,
# 		image TEXT,
# 		available INTEGER,
# 		categoryId INTEGER,
# 		userId INTEGER,
# 		FOREIGN KEY(userId) REFERENCES users(userId)
# 		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
# 		)''')

# conn.execute('''CREATE TABLE categories
# 		(categoryId INTEGER PRIMARY KEY,
# 		name TEXT
# 		)''')

conn.execute('''INSERT INTO users (password, email, name, phone)
    VALUES ("123456" , "test@gmail.com" , "DoanMinhTruong" , "0123321");''')

conn.execute('''
    INSERT INTO categories(name) VALUES ("Vật dụng sinh hoạt");
''')
conn.execute('''
    INSERT INTO categories(name) VALUES ("Đồ dùng học tập");
''')
conn.execute('''
    INSERT INTO categories(name) VALUES ("Quần áo");
''')


conn.close()
print("SEEDING DONE")