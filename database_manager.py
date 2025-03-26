# database_manager.py

import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

import config  # Import config

# Initialize embeddings using environment variable (set in config.py)
embedding = OpenAIEmbeddings()

try:
    vectorstore = Chroma(embedding_function=embedding, persist_directory=config.CHROMA_PERSIST_DIR)
except:
    vectorstore = Chroma(embedding_function=embedding, persist_directory=config.CHROMA_PERSIST_DIR)

def store_scenario(scenario_text, decision_code=None, evaluation=None):
    metadata = {}
    if decision_code is not None:
        metadata["decision_code"] = str(decision_code)
    if evaluation:
        metadata["evaluation"] = evaluation

    doc = Document(
        page_content=scenario_text,
        metadata=metadata
    )
    vectorstore.add_documents([doc])
    vectorstore.persist()

def retrieve_similar_scenarios(query_text):
    # Use config.NUM_SIMILAR_SCENARIOS as k
    return vectorstore.similarity_search(query_text, k=config.NUM_SIMILAR_SCENARIOS)

