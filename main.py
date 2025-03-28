from fastapi import FastAPI, HTTPException, Query
import json
import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Updated import
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage
from langchain.docstore.in_memory import InMemoryDocstore

app = FastAPI()

DATA_FILE = "indexed_data.json"

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        indexed_data = json.load(f)
else:
    indexed_data = {}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(indexed_data, f, indent=4)

# ✅ Check API key
OPENAI_API_KEY = os.getenv("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")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing. Set it in environment variables.")

# ✅ Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4", temperature=0.5, openai_api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# ✅ Initialize FAISS Vector Store
dimension = 1536  # OpenAI embedding size
index = faiss.IndexFlatL2(dimension)
vector_store = FAISS(embedding_model, index, InMemoryDocstore({}), {})

# ✅ Initialize memory for conversations
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# ✅ Intelligent search with FAISS
@app.get("/intelligent-search/")
def intelligent_search(query: str = Query(..., description="Enter search query")):
    # Step 1: Check direct match in indexed data
    if query in indexed_data:
        return {"query": query, "result": indexed_data[query]}

    # Step 2: Search in FAISS vector store
    query_embedding = embedding_model.embed_query(query)
    search_results = vector_store.similarity_search_by_vector(query_embedding, k=3)

    if search_results:
        return {"query": query, "result": [doc.page_content for doc in search_results]}

    # Step 3: Use LLM for reasoning
    system_message = SystemMessage(content="You are an AI search assistant.")
    user_message = HumanMessage(content=f"Find relevant information for: {query}")

    response = llm([system_message, user_message])
    result = response.content

    return {"query": query, "suggested_result": result}


# ✅ Insert new data & update FAISS
@app.post("/insert/")
def insert_data(key: str, value: str):
    indexed_data[key] = value
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(indexed_data, f, indent=4)

    # Update FAISS index
    vector_store.add_texts([value])

    return {"message": "Data inserted successfully", "data": indexed_data}


# ✅ Default route
@app.get("/")
def read_root():
    return {"message": "FastAPI server with FAISS search is running 🚀"}
