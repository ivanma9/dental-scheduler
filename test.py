from db import CosmosDB
import json


def main():
    db = CosmosDB()
    # Describe schema using SQL-like query
    results = db.query_appointments("SELECT c.Time FROM c ORDER BY c.Time ASC")

    print(json.dumps(results, indent=2))


    results = db.query_appointments("SELECT * FROM c WHERE DateTimePart('weekday', c.Time) = 6 ORDER BY c.Time ASC")

    
    print(json.dumps(results, indent=2))

def infer_schema(document):
    schema = {}
    for key, value in document.items():
        schema[key] = type(value).__name__
    return schema


if __name__ == "__main__":
    main()