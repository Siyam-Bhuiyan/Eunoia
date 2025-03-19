from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import traceback


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("Please set PINECONE_API_KEY in your .env file")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

try:
    print("Loading PDF files...")
    extracted_data=load_pdf_file(data='Data/')
    print(f"Loaded {len(extracted_data)} documents")
    
    print("Splitting text into chunks...")
    text_chunks=text_split(extracted_data)
    print(f"Created {len(text_chunks)} text chunks")
    
    print("Downloading embeddings...")
    embeddings = download_hugging_face_embeddings()
    print("Embeddings downloaded successfully")

    print("Initializing Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    index_name = "medicalbot"
    
    # Check if index exists
    existing_indexes = pc.list_indexes()
    if index_name in [index.name for index in existing_indexes]:
        print(f"Index '{index_name}' already exists")
    else:
        print(f"Creating new index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=384, 
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )
        print(f"Index '{index_name}' created successfully")

    print("Creating vector store...")
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings, 
    )
    print("Vector store created successfully")

except Exception as e:
    print("Error occurred:")
    print(traceback.format_exc())
    raise
