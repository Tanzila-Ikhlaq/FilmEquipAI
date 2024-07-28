import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("film_equipment.db")
c = conn.cursor()

# Create tables
c.execute('''
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        availability BOOLEAN
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        rating INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS assistance_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        equipment_id INTEGER NOT NULL,
        issue_description TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (equipment_id) REFERENCES equipment(id)
    )
''')

# Populate tables with sample data
c.execute('''
    INSERT INTO equipment (name, type, price, availability)
    VALUES
    ('Camera A', 'Camera', 150.00, 1),
    ('Camera B', 'Camera', 200.00, 1),
    ('Tripod A', 'Accessory', 50.00, 1),
    ('Tripod B', 'Accessory', 60.00, 1),
    ('Tripod C', 'Accessory', 70.00, 0),
    ('Microphone A', 'Audio', 75.00, 1),
    ('Microphone B', 'Audio', 85.00, 0),
    ('Microphone C', 'Audio', 95.00, 1),
    ('Lighting Kit A', 'Lighting', 200.00, 1),
    ('Drone A', 'Drone', 500.00, 1),
    ('Drone B', 'Drone', 550.00, 1),
    ('Drone C', 'Drone', 600.00, 0)
''')

c.execute('''
    INSERT INTO customers (name, email, phone)
    VALUES
    ('Alice Smith', 'alice@example.com', '123-456-7890'),
    ('Bob Johnson', 'bob@example.com', '098-765-4321'),
    ('Charlie Brown', 'charlie@example.com', '555-555-5555')
''')

c.execute('''
    INSERT INTO reviews (customer_id, review_text, rating, date)
    VALUES
    (1, 'Great camera, very satisfied!', 5, '2023-07-20'),
    (2, 'The microphone quality was poor.', 2, '2023-07-21'),
    (3, 'The lighting kit was perfect for my needs.', 4, '2023-07-25')
''')

c.execute('''
    INSERT INTO assistance_requests (customer_id, equipment_id, issue_description, date, status)
    VALUES
    (1, 1, 'Camera not turning on', '2023-07-22', 'Pending'),
    (2, 2, 'Tripod legs are stuck', '2023-07-23', 'Pending'),
    (3, 4, 'Lighting kit not working', '2023-07-24', 'Pending')
''')

# Commit changes and close connection
conn.commit()
conn.close()
