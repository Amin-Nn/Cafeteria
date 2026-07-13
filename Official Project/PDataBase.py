import sqlite3
import os


db_path = os.path.join(os.path.dirname(__file__), 'cafeteria.db')


connection = sqlite3.connect(db_path)
cursor = connection.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    page INTEGER NOT NULL,
                    available INTEGER DEFAULT 1
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    comment TEXT,
                    FOREIGN KEY (item_id) REFERENCES menu_items(id)
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    message TEXT
                )''')


cursor.execute('SELECT COUNT(*) FROM menu_items')
if cursor.fetchone()[0] == 0:
    
    breakfast_items = [
        ('Pancakes', 'Breakfast', 'Fluffy pancakes with syrup', 5.99, 2),
        ('Eggs & Toast', 'Breakfast', 'Scrambled eggs with buttered toast', 4.99, 2),
        ('Oatmeal', 'Breakfast', 'Warm oatmeal with berries', 4.49, 2),
        ('Breakfast Sandwich', 'Breakfast', 'Bacon, egg, and cheese sandwich', 6.49, 2),
    ]
    
    
    lunch_items = [
        ('Grilled Chicken', 'Lunch', 'Seasoned grilled chicken with vegetables', 8.99, 3),
        ('Beef Burger', 'Lunch', 'Classic burger with fries', 7.99, 3),
        ('Caesar Salad', 'Lunch', 'Fresh caesar salad with croutons', 7.49, 3),
    ]
    
    
    snacks_items = [
        ('French Fries', 'Snacks', 'Crispy golden fries', 3.49, 4),
        ('Popcorn', 'Snacks', 'Fresh buttered popcorn', 3.99, 4),
        ('Coffee', 'Beverages', 'Fresh brewed coffee', 2.49, 4),
        ('Iced Tea', 'Beverages', 'Cold iced tea', 2.99, 4),
        ('Smoothie', 'Beverages', 'Fruit smoothie blend', 4.99, 4),
    ]
    
    
    dessert_items = [
        ('Chocolate Cake', 'Desserts', 'Rich chocolate cake slice', 4.99, 5),
        ('Ice Cream', 'Desserts', 'Various ice cream flavors', 3.99, 5),
        ('Cheesecake', 'Desserts', 'Classic NY cheesecake', 5.49, 5),
        ('Cookies', 'Desserts', 'Homemade cookies', 2.99, 5),
    ]
    
    cursor.executemany('INSERT INTO menu_items (name, category, description, price, page) VALUES (?, ?, ?, ?, ?)',
                       breakfast_items + lunch_items + snacks_items + dessert_items)


connection.commit()
connection.close()

def get_db_connection():
    """Get a database connection"""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection