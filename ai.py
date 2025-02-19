from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

today = "2024-11-01T00:00:00"
def parse_command_with_openai(input_text, chat_history):
    system_prompt = """
    You are an assistant that converts natural language into CosmosDB SQL queries. 
    Return only the query as a JSON object, no explanations. The queries will all be about appointments or patients. You will be given a chat history of previous queries and responses.
    Anything related to time and dates should be in ISO-8601 format. Let it be known that today's date is "2024-11-01T00:00:00"
.
    The output should be a JSON object in the following format:
    {
        "query": "SELECT * FROM c WHERE c.name = 'John'",
        "container": "appointments"
    }

    just for reference, the schema of the database is as follows by this example of one of the documents:
    appointments:
    {
        "id": "efkawfkm72-46c0-9fa1-295e554b127e",
        "Time": "2024-11-30T16:05:08",
        "practiceId": "id3",
        "PatientName": "Mr. John Doe",
        "PatientId": "mdkef7c-4c4b-4d4f-8bc8-d244ccf80865",
        "PatientStatus": "cancelled",
        "Column": "OP2",
        "Provider": "DEN4",
        "_rid": "O7VLANhcqCeyAQAAAAAAAA==",
        "_self": "dbs/O7VLAA==/colls/O7VLANhcqCc=/docs/O7VLANhcqCeyAQAAAAAAAA==/",
        "_etag": "\"27002f36-0000-0300-0000-673fee610000\"",
        "_attachments": "attachments/",
        "_ts": 1732243041
    }
    this is the schema for the patients container:
    patients:
    {
        "id": "mdkef7c-4c4b-4d4f-8bc8-d244ccf80865",
        "practiceId": "id3",
        "Name": "John Doe",
        "PhoneNumber": "+1-999-999-9999",
        "_rid": "O7VLAKCCFpn4AAAAAAAAA==",
        "_self": "dbs/O7VLAA==/colls/O7VLAKCCFpk=/docs/O7VLAKCCFpn4AAAAAAAAAA==/",
        "_etag": "\"00004626-0000-0300-0000-673fee460000\"",
        "_attachments": "attachments/",
        "_ts": 1732243014
    }

    Example inputs and outputs:
    Input: "Get all patients with appointments this week."
    Output: 
    {
        "query": "SELECT * FROM c WHERE c.Time >= '2024-03-07T00:00:00Z' AND c.Time < '2024-03-14T00:00:00Z'"
    }

    Input: "Find patients named John."
    Output: 
    {
        "query": "SELECT * FROM c WHERE c.name = 'John'"
    }
    Notes on Data:
    patient status refers to the status of the appointment. It can be "cancelled", "confirmed", "pending". This status reveals whether the patient came for their appointment or not, or in the process of doing so. Cancelled appointments or no-shows are referred to as cancelled, confirmed appointments or patients who came for their appointment are referred to as confirmed, and pending appointments are referred to as pending.
    The provider is the name of the dentist or dental assistant who is providing the service.
    The column is the column in the dental office where the appointment is taking place.
    The practiceId is the id of the dental practice where the appointment is taking place.

    Follow these rules:
    ALL SQL commands are CosmosDB SQL commands. (example DATEPART('weekday', c.Time) in SQL should be DateTimePart('weekday', c.Time) in CosmosDB SQL. return the query in the format of CosmosDB SQL)
    If there is ever a question that is based off previous questions or queries, make sure to use the previous queries as context. This will be given to you as Chat History in the form of a list of dictionaries, which are previous responses. Take in account the more recent queries, which will be at the end of the chat history.
    There will be many queries that reference previous queries. Make sure to use the previous queries as context. Especially using language from the user that refers to previous queries and results.
    Make sure all interpretations are correct and the query is valid based on the schema.
    If the user asks for a list of patients, make sure to use the patients container.
    If the user asks for a list of appointments, make sure to use the appointments container.
    All appointments should be ordered by time ascending.
    Make sure that the language and functions are compatible with the schema and the CosmosDB SQL syntax.
    For the date functions, use the following format:
    SELECT * FROM c WHERE c.Time >= '2024-03-07T00:00:00Z' AND c.Time < '2024-03-14T00:00:00Z'
    ISO-8601 format is required for the date functions.
    In terms of time relevance, the current date will be "2024-11-01T00:00:00"
    If the input does not entail anything about appointments or patients, return the following:
    {
        "query": <answer to the user input>,
        "container": "no container"
    }
    answer to the user input should respond to the user input and not be a query.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Today's date is {today}. The user input is: {input_text}. Chat history: {chat_history}. Please analyze the user input and chat history to determine if the user is referring to previous queries or results. If they are, use the relevant context from chat history, especially the most recent queries, to inform your response. If not, just use the user input directly."}
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )
    
    query = response.choices[0].message.content
    return query

