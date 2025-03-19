from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import traceback

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Please set PINECONE_API_KEY and OPENAI_API_KEY in your .env file")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medicalbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

system_prompt = (
    "You are a helpful medical chatbot assistant. Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the "
    "answer concise. Always provide accurate medical information based on the context provided."
    "\n\n"
    "{context}"
)

llm = OpenAI(temperature=0.4, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input = msg
        print("User input:", input)
        response = rag_chain.invoke({"input": msg})
        print("Response:", response["answer"])
        return str(response["answer"])
    except Exception as e:
        print("Error occurred:")
        print(traceback.format_exc())
        return f"I apologize, but I encountered an error processing your request: {str(e)}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
