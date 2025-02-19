# dental-scheduler


Create a virtual environment with 
```
python -m venv venv
```

Activate the virtual environment with 
```
source venv/bin/activate
```

Install the requirements with 
```
pip install -r requirements.txt
```

Install all the python packages with 
```
pip install -r requirements.txt
```

Make sure to set the `COSMOS_CONNECTION_STRING` environment variable and the OpenAI API key in your `.env` file.

To run the app, run 
```
python main.py
```

You can set it yourself, but I made the default today's date be `2024-11-01T00:00:00` which November 1st, 2024.


## Schema

### appointments

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
},

### patients

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
