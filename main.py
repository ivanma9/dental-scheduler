import argparse
import json
import openai
from db import CosmosDB
from ai import parse_command_with_openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

def greet_user():
    print("Welcome to the CosmosDB Chat CLI!")
    print("You can ask me to perform operations like querying appointments.")
    print("Type 'exit' to quit the chat.")

def execute_command(SQL_command, db):
    results = db.query_appointments(SQL_command)
    print(f"Query results: {json.dumps(results, indent=2)}")

def main():
    db = CosmosDB()
    greet_user()
    
    while True:
        user_input = input("You: ")
        if "exit" in user_input:
            print("Goodbye!")
            break
        SQL_command = parse_command_with_openai(user_input)

        execute_command(SQL_command, db)

if __name__ == '__main__':
    main()
