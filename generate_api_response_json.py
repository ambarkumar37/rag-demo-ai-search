import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
import json
from dotenv import load_dotenv

from openai import AzureOpenAI

# load_dotenv("./.env", override=True)

# api_key = os.getenv("AZURE_AI_KEY")
# endpoint_ai = os.getenv("AZURE_AI_ENDPOINT")
# api_key_ai_search = os.getenv("AI_SEARCH_KEY")
# endpoint_ai_search = os.getenv("AI_SEARCH_ENDPOINT")
# search_index_name = os.getenv("AI_SEARCH_INDEX")
# deployment = os.getenv("AI_MODEL_DEPLOYMENT_NAME")
# api_version = "2024-12-01-preview"

# client = AzureOpenAI(
#     api_version=api_version,
#     azure_endpoint=endpoint_ai,
#     api_key=api_key,
# )


client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=AI_FOUNDRY_AI_SERVICES_URL,
    api_key=AI_FOUNDRY_KEY,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are an expert in the economic theory or Henry George. An american economist of the 19 century",
        },
        {
            "role": "user",
            "content": "What is the main proposition for the solving the problem of poverty?",
        }
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": AZURE_SEARCH_ENDPOINT,
                    "index_name": "progress-poverty-index",
                    "authentication": {
                        "type": "api_key",
                        "key": AZURE_SEARCH_API_KEY,
                    },
                    "top_n_documents":3,
                 "fields_mapping": {
                    "title_field": "chapter_name",     
                    "filepath_field": "file",          
                    "content_fields": ["chunk_content", "book", "chapter_name"],
                    "vector_fields": ["vector"],
                }  
                }
            }
        ]
    },
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=gpt4deployment
)

print(response.to_dict()["choices"])


with open("response.json", "w") as f:
    json.dump(response.to_dict(), f, indent=4)
