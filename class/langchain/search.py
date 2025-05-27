from http import client
from dotenv import load_dotenv
import os
import meilisearch

load_dotenv()

client = meilisearch.Client(
    os.getenv("MEILI_SEARCH_URL"), 
    os.getenv("MEILI_SEARCH_API_KEY")
    )
def stock_search(query):
    return client.index("nasdaq").search(query)