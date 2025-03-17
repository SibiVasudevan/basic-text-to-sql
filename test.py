import os
db_path = os.path.join(os.path.dirname(__file__), "sample_database.db")
print(f"Database path: {db_path}")
print(f"Exists: {os.path.exists(db_path)}")