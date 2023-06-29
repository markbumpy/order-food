import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurant (
        id INTEGER PRIMARY KEY,
        food_name TEXT,
        price INTEGER,
        quantity INTEGER)''')

foods = [
    ('pizza', 200, 3),
    ('jollof rice', 250, 3),
    ('fried rice', 500, 3)
]

for food in foods:
    cursor.execute('INSERT INTO restaurant (food_name, price, quantity) VALUES (?,?,?)', food)

conn.commit()
conn.close()
