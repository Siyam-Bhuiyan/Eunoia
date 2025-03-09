from setuptools import setup, find_packages

setup(
    name="eunoia",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sentence-transformers",
        "langchain",
        "flask",
        "pypdf",
        "python-dotenv",
        "pinecone-client",
        "langchain-pinecone",
        "langchain_community",
        "langchain_openai",
        "langchain_experimental"
    ]
)
