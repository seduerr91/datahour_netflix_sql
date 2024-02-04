from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
import pandas as pd
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def prepare_spider_data(data_location, database_location):
    print("## Ingesting Spider data into a vectorstore. ##")
    df = pd.read_csv(data_location, sep='\t', index_col=0)
    loader = DataFrameLoader(df, page_content_column="Masked Questions")
    documents = loader.load()
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    Chroma.from_documents(documents, embedding_function, persist_directory=database_location)
    print("## Completed ingestion of vectorstore. ##")


def prepare_spider_data_faiss(data_location, database_location):
    print("## Ingesting Spider data into a FAISS vectorstore. ##")
    df = pd.read_csv(data_location, sep='\t', index_col=0)
    loader = DataFrameLoader(df, page_content_column="Masked Questions")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(f"{database_location}/" + "faiss_index")
    print("## Completed ingestion of vectorstore. ##")