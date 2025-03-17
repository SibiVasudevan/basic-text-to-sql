import sqlite3
import os

db_schema = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    signup_date DATE,
    last_login TIMESTAMP
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category TEXT,
    inventory INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""

def initialize_database(db_path="sample_database.db"):
    """Initialize the SQLite database with schema and sample data if not already present."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]

        # Create tables if they don't exist
        for statement in db_schema.strip().split(';'):
            if statement.strip():
                table_name = statement.strip().split()[2]  # Extract table name from "CREATE TABLE <name>"
                if table_name not in existing_tables:
                    cursor.execute(statement)

        # Sample data to insert only if tables are empty
        sample_data = [
            ("users", """
            INSERT INTO users (id, name, email, signup_date, last_login) VALUES
            (1, 'John Smith', 'john@example.com', '2023-01-15', '2023-03-20 14:30:00'),
            (2, 'Sarah Johnson', 'sarah@example.com', '2023-02-20', '2023-03-21 09:15:00'),
            (3, 'Michael Brown', 'michael@example.com', '2023-01-30', '2023-03-19 16:45:00'),
            (4, 'Emily Davis', 'emily@example.com', '2023-03-05', '2023-03-22 11:20:00'),
            (5, 'David Wilson', 'david@example.com', '2023-02-10', '2023-03-18 13:10:00')
            """),
            ("products", """
            INSERT INTO products (id, name, price, category, inventory) VALUES
            (1, 'Laptop', 999.99, 'Electronics', 45),
            (2, 'Smartphone', 699.99, 'Electronics', 120),
            (3, 'Coffee Maker', 79.99, 'Kitchen', 30),
            (4, 'Running Shoes', 129.99, 'Clothing', 75),
            (5, 'Headphones', 149.99, 'Electronics', 60)
            """),
            ("orders", """
            INSERT INTO orders (id, user_id, order_date, total_amount) VALUES
            (1, 1, '2023-03-10 10:30:00', 999.99),
            (2, 2, '2023-03-12 14:45:00', 229.98),
            (3, 3, '2023-03-15 09:20:00', 699.99),
            (4, 4, '2023-03-18 16:10:00', 279.98),
            (5, 1, '2023-03-20 11:05:00', 149.99)
            """),
            ("order_items", """
            INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
            (1, 1, 1, 999.99),
            (2, 3, 1, 79.99),
            (2, 5, 1, 149.99),
            (3, 2, 1, 699.99),
            (4, 3, 1, 79.99),
            (4, 4, 1, 129.99),
            (5, 5, 1, 149.99)
            """)
        ]

        # Insert sample data only if tables are empty
        for table, data in sample_data:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            if cursor.fetchone()[0] == 0 and data.strip():
                cursor.execute(data)

        conn.commit()
        conn.close()
        print("Database initialized or verified successfully.")
        return True
    except sqlite3.Error as e:
        print(f"SQLite error during initialization: {e}")
        return False
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def execute_sql_query(sql_query, db_path="sample_database.db"):
    """Execute an SQL query and return results with column names."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        if column_names:
            results = cursor.fetchall()
        else:
            conn.commit()
            results = "Query executed successfully."
        conn.close()
        return results, column_names
    except sqlite3.Error as e:
        return f"SQLite error: {e}", None
    except Exception as e:
        return f"Error executing query: {e}", None