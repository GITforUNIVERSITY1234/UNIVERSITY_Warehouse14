import sqlite3
from contextlib import contextmanager # для бд с автоматическим закрытием

DATABASE = 'warehouse.db'

@contextmanager
def get_db(): # Подключение к бд с автоматическим закрытием
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db(): # Создание бд
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                supplier TEXT NOT NULL
            )
        ''')

def get_products(sort_by=None, category_filter=None, low_stock_threshold=None):
    with get_db() as db:
        query = 'SELECT * FROM products'
        params = []
        
        # Фильтр по категории
        if category_filter and category_filter != 'all':
            query += ' WHERE category = ?'
            params.append(category_filter)
        
        # Фильтр для low_stock
        if low_stock_threshold is not None:
            query += ' WHERE quantity <= ?'
            params.append(low_stock_threshold)
        
        # Сортировка
        if sort_by == 'price_asc':
            query += ' ORDER BY price ASC'
        elif sort_by == 'price_desc':
            query += ' ORDER BY price DESC'
        elif sort_by == 'quantity_asc':
            query += ' ORDER BY quantity ASC'
        elif sort_by == 'quantity_desc':
            query += ' ORDER BY quantity DESC'
        else:
            query += ' ORDER BY id DESC'
        
        return db.execute(query, params).fetchall()

def get_product(product_id): # товар по id
    with get_db() as db:
        return db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

def add_product(name, category, quantity, price, supplier): # добавление
    with get_db() as db:
        db.execute('''
            INSERT INTO products (name, category, quantity, price, supplier)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, quantity, price, supplier))

def update_product(product_id, name, category, quantity, price, supplier): # изменение
    with get_db() as db:
        db.execute('''
            UPDATE products 
            SET name = ?, category = ?, quantity = ?, price = ?, supplier = ?
            WHERE id = ?
        ''', (name, category, quantity, price, supplier, product_id))

def update_quantity(product_id, new_quantity): # изменение кол-ва
    with get_db() as db:
        db.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))

def delete_product(product_id):
    with get_db() as db:
        db.execute('DELETE FROM products WHERE id = ?', (product_id,))

def get_categories():
    with get_db() as db:
        categories = db.execute('SELECT DISTINCT category FROM products ORDER BY category').fetchall()
        return [cat['category'] for cat in categories]