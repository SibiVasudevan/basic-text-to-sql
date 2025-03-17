import sys
from database import initialize_database, execute_sql_query, db_schema
from app import generate_sql_query

def main():
    print("Checking and initializing database if needed...")
    if not initialize_database():
        print("Failed to initialize database. Exiting.")
        sys.exit(1)

    print("Text-to-SQL CLI")
    print("Database Schema:")
    print(db_schema)
    print("Enter natural language to convert to SQL and query the database")
    print("Enter 'quit' or 'exit' to exit.")
    while True:
        user_query = input("> ")
        if user_query.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        sql_query = generate_sql_query(user_query)
        print("\nGenerated SQL Query:")
        print(sql_query)

        if "select" in sql_query.lower():
            results, columns = execute_sql_query(sql_query)
            if columns:
                print("\nResults:")
                print(" | ".join(columns))
                print("-" * 50)
                for row in results:
                    print(" | ".join(str(item) for item in row))
            else:
                print(f"\nError: {results}")
        else:
            print("\nNon-SELECT query not executed for safety.")

if __name__ == "__main__":
    main()