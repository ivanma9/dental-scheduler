import json
from db import CosmosDB
from ai import parse_command_with_openai
from datetime import datetime
from tabulate import tabulate


today = "2024-11-01T00:00:00"


def greet_user():
    print("Welcome to the CosmosDB Chat CLI!")
    print("You can ask me to perform operations like querying appointments.")
    print(f"Today's date is: {today.split('T')[0]}")


def execute_command(SQL_command, db, container):
    print(f"Executing command: {SQL_command}")
    print(f"Container: {container}")
    if container == "appointments":
        results = db.query_appointments(SQL_command)
        columns = ['Time', "Day",'PatientName', 'PatientStatus', 'practiceId', 'Column', 'Provider', 'PatientId']
    elif container == "patients":
        results = db.query_patients(SQL_command)
        columns = ['id', 'Name', 'PhoneNumber', 'practiceId']
    display_appointment_results(results, columns)
    print("Here are the results for your query. Is there anything else you would like to know?")
    return results

def display_appointment_results(results, columns):
    # Check if results is empty
    if not results:
        print("No results found for your query.")
        return

    # Format the results
    formatted_results = []
    for row in results:
        if 'Time' in row:
            row['Time'] = datetime.fromisoformat(row['Time'].replace('Z', '')).strftime('%Y-%m-%d %H:%M')
            row['Day'] = datetime.fromisoformat(row['Time'].replace('Z', '')).strftime('%a')
        formatted_row = [row.get(col, '') for col in columns]
        formatted_results.append(formatted_row)

    # Print the table
    print(tabulate(formatted_results, headers=columns, tablefmt='grid'))

def main():
    db = CosmosDB()
    greet_user()
    chat_history = []
    while True:
        print("Type 'exit' to quit the chat.")
        user_input = input("You: ")
        if "exit" in user_input:
            print("Goodbye!")
            break
        response = json.loads(parse_command_with_openai(user_input, chat_history))
        SQL_command = response["query"]
        container = response["container"]
        chat_history.append(response)
        if "no container" in container:
            print(SQL_command)
        else:
            results = execute_command(SQL_command, db, container)
        

if __name__ == '__main__':
    main()
