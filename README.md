# RAG PIPELINE


### Create a AIServices

[documentation](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal)

### Deploy a Chat Completion Model

`gpt-4o`


### Deploy an embeding model

`text-embedding-3-large`


### Create a .env file

```sh
AZURE_AI_KEY=<your_api_key>
AZURE_AI_ENDPOINT=https://<yourinstance>.cognitiveservices.azure.com/
AZURE_AI_ENDPOINT_EMBEDDINGS=https://<yourinstance>.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large
EMBEDDINGS_MODEL_DEPLOYMENT=text-embedding-3-large
EMBEDDINGS_MODEL=text-embedding-3-large
AI_SEARCH_KEY=<your_admin_key>
AI_SEARCH_ENDPOINT=https://<yourinstance>.search.windows.net
AI_SEARCH_INDEX=progress-poverty-index
AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### Setup local python enviroment with UV

#### Install Dependencies

create requirements.txt

```txt
azure-ai-inference 
azure-core 
azure-search-documents 
dotenv
openai
tiktoken
```

`uv init`

`uv add -r requemements.txt`


### Pipeline steps

file `main.py`

#### STEP 1 -  Split the chapters and save them to files

uses `split_chapters`

#### STEP 2 Create the chapters from the JSON file

uses `get_chunk_object` 

#### STEP 3 - Create the search index

uses `create_search_index`

#### STEP 4 - Upload the chunks to the search index

uses `upload_chunk_document`

### RAG

file `rag.py`

uses `get_response`

```python
messages = [{
            "role": "system",
            "content": "You are an expert in the economic theory or Henry George. An american economist of the 19 century",
    }]


while True:
    user_input = input("User: what is your question? (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})

    client = get_openai_client()

    response = get_response(messages)
    print(response.choices[0].message.content)
    citations = response.choices[0].message.context["citations"]
    if citations:
        print("Citations:")
        for citation in citations:
            print(f" - {citation['title']}: {citation['filepath']}")
    else:
        print("No citations found.")
    messages.append({"role": "assistant", "content": response.choices[0].message.content})


