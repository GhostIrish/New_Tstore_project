import os
from flask import Flask, jsonify, request
import sqlite3
from main import MainApplication

# Load environment variables from .env file
DATABASE_FILE = 'styledb.db'
app = Flask(__name__)

# Establish connection with the MySQL database
def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row  # For dict-like access to rows
    return connection

# Fetch product information from the database
@app.route('/api/products', methods=['GET'])
def get_products():
    query = request.args.get('query', '')
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        query_sql = ''' 
                SELECT p.id, p.model_product, pt.type_name as product_type, s.size_name as size, gp.gender, 
                b.brand_name as brand, p.buying_price, p.selling_price, p.quantity 
                FROM product p
                JOIN product_types pt ON p.product_type = pt.id
                JOIN sizes s ON p.size = s.id
                JOIN gender_products gp ON p.gender_product = gp.id
                JOIN brands b ON p.brand = b.id
                '''
        if query:
            query_sql += "WHERE p.model_product LIKE ?"
            search_query = (query + '%',)
            cursor.execute(query_sql, search_query)
        else:
            cursor.execute(query_sql)
        products = [dict(row) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return jsonify({"error": "An error occurred while fetching products"}), 500
    finally:
        connection.close()
        
    return jsonify(products)

# Insert a new product into the database
@app.route('/api/add_product', methods=['POST'])
def add_product():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        new_product = request.json
        

        sql = '''
        INSERT INTO product (model_product, product_type, size, gender_product, brand, buying_price, selling_price, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            new_product['model_product'], 
            new_product['product_type'], 
            new_product['size'], 
            new_product['gender_product'], 
            new_product['brand'], 
            new_product['buying_price'], 
            new_product['selling_price'], 
            new_product['quantity']
        ))
        connection.commit()
            
        return jsonify(message='Product registered successfully', item=new_product), 201

    except sqlite3.Error as error:
        return jsonify(error=str(error)), 500
    finally:
        connection.close()

# Update existing product information in the database
@app.route('/api/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        updated_product = request.json
        print(f'received data: {updated_product}')

        sql = '''
        UPDATE product 
        SET model_product = ?, product_type = ?, size = ?, gender_product = ?, brand = ?, buying_price = ?, selling_price = ?, quantity = ?
        WHERE id = ?
            '''
        cursor.execute(sql, (
            updated_product['model_product'],
            updated_product['product_type'],
            updated_product['size'],
            updated_product['gender_product'],
            updated_product['brand'],
            updated_product['buying_price'],
            updated_product['selling_price'],
            updated_product['quantity'],
            product_id
        ))
        connection.commit()
            
        return jsonify(message='Product updated successfully', item=updated_product), 200

    except sqlite3.Error as error:
        return jsonify(error=str(error)), 500
    finally:
        connection.close()

# Fetch product types for use in the UI's option menu
@app.route('/api/types', methods=['GET'])
def get_product_types():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id, type_name FROM product_types')
        types = [dict(row) for row in cursor.fetchall()]
        return jsonify(types)
    
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred while fetching product types'}), 500
    finally:
        connection.close()

# Fetch sizes for use in the UI's option menu
@app.route('/api/sizes', methods=['GET'])
def get_sizes():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id, size_name FROM sizes')
        sizes = [dict(row) for row in cursor.fetchall()]
        return jsonify(sizes)
    
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred while fetching sizes'}), 500
    finally:
        connection.close()
    
# Fetch gender options for use in the UI's option menu
@app.route('/api/genders', methods=['GET'])
def get_genders():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, gender FROM gender_products')
            genders = cursor.fetchall()
        return jsonify(genders)
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred while fetching genders'}), 500
    finally:
        connection.close()
    
# Fetch brand options for use in the UI's option menu
@app.route('/api/brands', methods=['GET'])
def get_brands():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id, brand_name FROM brands')
        brands = [dict(row) for row in cursor.fetchall()]
        return jsonify(brands)
    
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return jsonify({'error': 'An error occurred while fetching brands'}), 500
    finally:
        connection.close()

# Delete a product from the database using its ID
@app.route('/api/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = 'DELETE FROM product WHERE id = ?'
        cursor.execute(sql, (product_id,))
        connection.commit()
        return jsonify(message=f'Product with id {product_id} deleted successfully'), 200
    
    except sqlite3.Error as error:
        return jsonify(error=str(error)), 500
    
    finally:
        connection.close()

# Entry point for running the Flask app (for testing purposes)
if __name__ == '__main__':
    app.run()
