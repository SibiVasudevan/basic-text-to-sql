import os
import requests
from dotenv import load_dotenv
from database import db_schema

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def query_anthropic_api(prompt):
    """Query the Anthropic API with a prompt and return the response."""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def generate_sql_query(natural_language_query):
    """Generate an SQL query from a natural language query."""
    prompt = f"""
    You are an expert SQL query generator. Given a database schema and a natural language query, 
    generate the corresponding SQL query. Return ONLY the SQL query with no explanation.

    Database Schema:
    {db_schema}

    Natural Language Query: {natural_language_query}

    SQL Query:
    """
    response = query_anthropic_api(prompt)
    return response["content"][0]["text"].strip() if response and "content" in response else "Failed to generate SQL query."