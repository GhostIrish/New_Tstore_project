import sqlite3, os


# creating a database file name
DATABASE_FILE = 'styledb.db'

# define table_name in db
TABLE_NAME = 'product'

# making connection with my database
connection = sqlite3.connect(DATABASE_FILE)
connection.execute("PRAGMA foreign_keys = ON") # activating fkeys
cursor = connection.cursor()

# all of this is for create a database and add all rules i need to this project.

cursor.execute(
    'CREATE TABLE IF NOT EXISTS product_types ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'type_name TEXT NOT NULL'
    ')'
)

cursor.execute(
    'CREATE TABLE IF NOT EXISTS sizes ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'size_name TEXT NOT NULL'
    ')'
)

cursor.execute(
    'CREATE TABLE IF NOT EXISTS gender_products ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'gender TEXT NOT NULL'
    ')'
)

cursor.execute(
    'CREATE TABLE IF NOT EXISTS brands ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'brand_name TEXT NOT NULL'
    ')'
)

cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'model_product TEXT NOT NULL, '
    'product_type INTEGER NOT NULL, '
    'size INTEGER NOT NULL, '
    'gender_product INTEGER NOT NULL, '
    'brand INTEGER NOT NULL, '
    'buying_price INTEGER NOT NULL, '
    'selling_price INTEGER NOT NULL, '
    'quantity INTEGER NOT NULL, '
    'FOREIGN KEY (product_type) REFERENCES product_types(id), '
    'FOREIGN KEY (size) REFERENCES sizes(id), '
    'FOREIGN KEY (gender_product) REFERENCES gender_products(id), '
    'FOREIGN KEY (brand) REFERENCES brands(id)'
    ')'
)

#insert INTEGERo support tables - :)
cursor.executemany(
    'INSERT INTO product_types (type_name) VALUES (?)',
    [('T-shirt',), ('Pants',), ('Jacket',), ('Shorts',), ('Coats',)]
)


cursor.executemany(
    'INSERT INTO sizes (size_name) VALUES (?)',
    [('PP',), ('P',), ('M',), ('G',), ('GG',), ('XXG',)]
)

cursor.executemany(
    'INSERT INTO gender_products (gender) VALUES (?)',
    [('Female',), ('Male',), ('Child',), ('Unisexual',)]
)

cursor.executemany(
    'INSERT INTO brands (brand_name) VALUES (?)',
    [('Nike',), ('Adidas',), ('Calvin Klein',), ('Gucci',), ]
)

# commit the changes
connection.commit()
 
 # closing the connection   
cursor.close()
connection.close()