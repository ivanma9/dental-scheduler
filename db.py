from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv
from pathlib import Path

class CosmosDB:
    def __init__(self):
        env_path = Path('.env')
        if not env_path.exists():
            print("Warning: .env file not found.")
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize CosmosDB client
        connection_string = os.environ.get('COSMOS_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("Please set COSMOS_CONNECTION_STRING environment variable")
        
        try:
            self.client = CosmosClient.from_connection_string(connection_string)
            self.database = self.client.get_database_client('Test1')
            self.patients = self.database.get_container_client('patients')
            self.appointments = self.database.get_container_client('appointments')
        except Exception as e:
            # Avoid exposing connection string in error messages
            raise Exception("Failed to connect to database. Please check your credentials.") from e

    def __str__(self):
        # Prevent accidental exposure of connection details
        return "CosmosDB Connection"

    def __repr__(self):
        # Prevent accidental exposure of connection details
        return "CosmosDB Connection"
    
    def query_patients(self, query):
        """Query patients using SQL-like syntax"""
        return list(self.patients.query_items(query=query, enable_cross_partition_query=True))

    def query_appointments(self, query):
        """Query appointments using SQL-like syntax"""
        return list(self.appointments.query_items(query=query, enable_cross_partition_query=True))
