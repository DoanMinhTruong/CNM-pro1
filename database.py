import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		name TEXT,
		phone TEXT
		)''')

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		available INTEGER,
		categoryId INTEGER,
		userId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId)
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')
		
import hashlib
conn.execute('INSERT INTO users (password, email, name, phone) VALUES (?, ?, ?, ?)', (hashlib.md5('123456'.encode()).hexdigest(), 'meir.truong.2309@gmail.com', 'DoanMinhTruong', '123456789'))

conn.execute('''
    INSERT INTO categories(name) VALUES ("Vật dụng sinh hoạt");
''')
conn.execute('''
    INSERT INTO categories(name) VALUES ("Đồ dùng học tập");
''')
conn.execute('''
    INSERT INTO categories(name) VALUES ("Quần áo");
''')
conn.commit()
conn.close()
print("CREATED DATABASE")