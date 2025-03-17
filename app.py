from flask import Flask, render_template, request, jsonify
from database import initialize_database, execute_sql_query
from api import generate_sql_query

app = Flask(__name__)

@app.route('/')
def index():
    initialize_database()  # Ensure DB exists on app start
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    data = request.json
    natural_language_query = data.get('query', '')
    if not natural_language_query:
        return jsonify({"error": "Query is required"}), 400

    sql_query = generate_sql_query(natural_language_query)
    execute_result = None
    if sql_query.lower().strip().startswith(('select', 'show')):
        results, columns = execute_sql_query(sql_query)
        execute_result = {"results": results, "columns": columns, "error": None} if columns else {"error": results}

    return jsonify({"sql_query": sql_query, "execution_result": execute_result})

if __name__ == '__main__':
    app.run(debug=True)