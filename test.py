from db import CosmosDB
import json
from tabulate import tabulate
from datetime import datetime


def display_appointment_results(db, query, columns):
    """
    Query the database and display results in a formatted table
    
    Args:
        db: CosmosDB instance
        query: str, the query to execute
        columns: list, the columns to display
    """
    results = db.query_appointments(query)

    # Format the results
    formatted_results = []
    for row in results:
        if 'Time' in row:
            row['Time'] = datetime.fromisoformat(row['Time'].replace('Z', '')).strftime('%Y-%m-%d %H:%M')
        formatted_row = [row.get(col, '') for col in columns]
        formatted_results.append(formatted_row)

    # Print the table
    print(tabulate(formatted_results, headers=columns, tablefmt='grid'))

def main():
    db = CosmosDB()
    
    # Define the columns we want to display
    columns = ['Time', 'PatientName', 'PatientStatus', 'practiceId', 'Column', 'Provider', 'PatientId']
    
    # Base query
    query = "SELECT c.Time, c.PatientName, c.PatientStatus, c.practiceId, c.Column, c.Provider, c.PatientId FROM c WHERE c.practiceId <> 'id3' ORDER BY c.Time ASC"
    
    # Display results twice (as in original code)
    display_appointment_results(db, query, columns)
    display_appointment_results(db, query, columns)

    results = db.query_patients("SELECT * FROM c WHERE c.Name = 'Anne Harrison'")
    print(results)

    # results = db.query_appointments("SELECT * FROM c WHERE DateTimePart('weekday', c.Time) = 6 ORDER BY c.Time ASC")
    # results = db.query_appointments("SELECT c.Time, c.PatientStatus FROM c WHERE c.PatientStatus = 'confirmed' ORDER BY c.Time ASC")

# #earliest appointments for each status
# #       {
# #     "Time": "2023-11-24T12:19:59",
# #     "PatientStatus": "pending"
# # #   },
#     # {
#     #   "Time": "2023-11-23T21:23:53",
#     #   "PatientStatus": "cancelled"
#     # },
# #       {
# #     "Time": "2023-11-26T14:44:26",
# #     "PatientStatus": "confirmed"
# #   },


def infer_schema(document):
    schema = {}
    for key, value in document.items():
        schema[key] = type(value).__name__
    return schema


if __name__ == "__main__":
    main()