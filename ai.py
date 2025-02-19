from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_command_with_openai(input_text, chat_history):
    system_prompt = """
    You are an assistant that converts natural language into CosmosDB SQL queries. 
    Return only the query, no explanations. The queries will all be about appointments or patients. You will be given a chat history of previous queries and responses.

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
    Output: SELECT * FROM c WHERE c.Time >= '2024-03-07T00:00:00Z' AND c.Time < '2024-03-14T00:00:00Z'

    Input: "Find patients named John."
    Output: SELECT * FROM c WHERE c.name = 'John'

    Follow these rules:
    If there is ever a question that is based off previous questions or queries, make sure to use the previous queries as context.
    Make sure all interpretations are correct and the query is valid based on the schema.
    If the user asks for a list of patients, make sure to use the patients container.
    If the user asks for a list of appointments, make sure to use the appointments container.
    Make sure that the language and functions are compatible with the schema and the CosmosDB SQL syntax.
    For the date functions, use the following format:
    SELECT * FROM c WHERE c.Time >= '2024-03-07T00:00:00Z' AND c.Time < '2024-03-14T00:00:00Z'
    ISO-8601 format is required for the date functions.
    In terms of time relevance, the current date will be
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=0
    )
    
    query = response.choices[0].message.content
    print(query)
    return query

