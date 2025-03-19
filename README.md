# Eunoia - Your Personal Healthcare Assistant

![Eunoia Medical Chatbot](insert_screenshot_path_here.png)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

Eunoia is an end-to-end medical chatbot built using LangChain, Pinecone vector database, and OpenAI's language models. It provides accurate and concise medical information by leveraging Retrieval-Augmented Generation (RAG) to answer healthcare-related questions based on verified medical content.

The chatbot features a modern, user-friendly interface with real-time responses and speech-to-text capabilities for enhanced accessibility.

## ✨ Features

- **Medical Knowledge Base**: Powered by curated medical documents for accurate information
- **Natural Language Understanding**: Process and understand medical queries in everyday language
- **Contextual Responses**: Provides relevant and accurate medical information
- **User-Friendly Interface**: Modern, responsive design for seamless interaction
- **Speech-to-Text**: Voice input option for enhanced accessibility
- **Real-time Communication**: Instant responses with typing indicators
- **Mobile Responsive**: Works on various devices and screen sizes
- **Fail-safe Responses**: Acknowledges when information is unavailable instead of providing incorrect data

## 🏗️ Architecture

Eunoia follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Text Embedding**: Medical documents are processed and embedded using Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model
2. **Vector Storage**: Embeddings are stored in Pinecone's vector database for efficient similarity search
3. **Query Processing**: User queries are embedded and used to retrieve relevant medical context
4. **Response Generation**: OpenAI's language model generates accurate responses based on the retrieved context
5. **Web Interface**: Flask-based web application with a responsive frontend

## 🛠️ Technology Stack

### Backend

- **Python 3.10+**: Core programming language
- **Flask**: Web framework for serving the application
- **LangChain**: Framework for building LLM applications
- **OpenAI API**: For generating accurate responses
- **Pinecone**: Vector database for storing and retrieving medical knowledge embeddings
- **Hugging Face Transformers**: For text embeddings
- **PyPDF**: For extracting text from medical PDFs

### Frontend

- **HTML/CSS/JavaScript**: Core web technologies
- **Bootstrap 5**: For responsive design
- **jQuery**: For AJAX and DOM manipulation
- **Font Awesome**: For icons
- **Web Speech API**: For speech-to-text functionality

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Pinecone API key
- OpenAI API key

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/eunoia-medical-chatbot.git
cd eunoia-medical-chatbot
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

#### For Windows:

```bash
venv\Scripts\activate
```

#### For macOS/Linux:

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create a .env file

Create a `.env` file in the root directory with the following content:

```
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Step 6: Prepare your medical data

Place your medical PDF documents in the `Data/` directory.

### Step 7: Set up Pinecone index

Run the data processing notebook to create and populate your Pinecone index:

```bash
jupyter notebook research/trials.ipynb
```

Execute the notebook cells to process documents and create the vector store.

## 💻 Usage

### Running the Application

Start the Flask application:

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:8080
```

### Interacting with the Chatbot

1. Type your medical question in the input field
2. Click the send button or press Enter to submit
3. Alternatively, click the microphone button to use speech-to-text
4. View the chatbot's response in the chat window

## 📁 Project Structure

```
eunoia-medical-chatbot/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Project dependencies
├── setup.py                # Package setup file
├── .env                    # Environment variables (not in version control)
│
├── src/                    # Source code directory
│   ├── __init__.py         # Package initialization
│   ├── helper.py           # Helper functions for document processing
│   └── prompt.py           # System prompts for the chatbot
│
├── templates/              # HTML templates
│   └── chat.html           # Main chat interface
│
├── static/                 # Static files
│   ├── style.css           # CSS styles
│   └── bot.png             # Chatbot icon
│
├── Data/                   # Directory for medical PDF documents
│   └── Medical_book.pdf    # Example medical reference
│
└── research/               # Research and development notebooks
    └── trials.ipynb        # Notebook for testing and setup
```

## ⚙️ How It Works

### 1. Data Processing

- Medical PDFs are loaded and split into manageable chunks
- Each chunk is processed using Hugging Face's embedding model
- Embeddings are stored in a Pinecone vector database

### 2. Query Handling

- When a user submits a question, their query is embedded using the same model
- The system searches the Pinecone index for the most semantically similar content
- The top 3 most relevant chunks are retrieved

### 3. Response Generation

- Retrieved medical information is passed to the OpenAI language model
- A carefully crafted system prompt ensures responses are:
  - Accurate based on the retrieved context
  - Concise (3 sentences maximum)
  - Clear about limitations (responds with "I don't know" when appropriate)

### 4. User Interface

- Flask serves the web application
- The frontend uses AJAX to send requests and update the chat interface
- Typing indicators provide feedback during processing
- Speech recognition allows for voice input

## ⚙️ Configuration

### System Prompt

The system prompt in `src/prompt.py` controls how the AI responds

### Text Splitting Parameters

In `src/helper.py`, you can configure how documents are split:

```python
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
```

### Retrieval Parameters

In `app.py`, you can adjust how many chunks are retrieved:

```python
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
