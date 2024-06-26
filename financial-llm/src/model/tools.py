import os
from pathlib import Path
from typing import List

from langchain.agents import Tool  # type: ignore
from langchain.chains import RetrievalQA # type: ignore
from langchain.chains.retrieval_qa.base import BaseRetrievalQA # type: ignore
from langchain.chat_models import ChatOpenAI # type: ignore
from langchain.document_loaders import PyPDFDirectoryLoader # type: ignore
from langchain.embeddings.openai import OpenAIEmbeddings # type: ignore
from langchain.llms import BaseLLM # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain.utilities import GoogleSerperAPIWrapper # type: ignore
from langchain.vectorstores import Chroma # type: ignore

# accessing ./data
ROOT_DIR = Path(__file__).absolute().parent.parent.parent


def setup_knowledge_base(llm: BaseLLM) -> BaseRetrievalQA:
    """
    Set up knowledge based on pdfs in data folder in root directory.
    Args:
        llm (BaseLLM): Language model used for retrieval chain.
    """

    if "db" in os.listdir("."):
        vectordb = Chroma(
            persist_directory="./db", embedding_function=OpenAIEmbeddings()
        )
    else:
        loader = PyPDFDirectoryLoader(str(ROOT_DIR) + "/data", silent_errors=True)
        documents = loader.load()
        for doc in documents:
            source = (
                doc.metadata["source"].removesuffix(".pdf").split("/")[-1].split("-")
            )
            product_name = source[1:-2]
            plan_type = source[-4:-2]
            doc.metadata["product_name"] = " ".join(product_name).title()
            doc.metadata["plan_type"] = " ".join(plan_type)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        documents = text_splitter.split_documents(documents)

        vectordb = Chroma.from_documents(
            documents, embedding=OpenAIEmbeddings(), persist_directory="./db"
        )
        vectordb.persist()

    knowledge_base = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 7}),
    )

    return knowledge_base


def get_tools():
    """
    Define tools usable by the Advisor Agent.
    """

    llm = ChatOpenAI(temperature=0)
    knowledge_base = setup_knowledge_base(llm)
    search = GoogleSerperAPIWrapper(type="news")
    tools = [
        Tool(
            name="WebSearch",
            func=search.run,
            description="Access to google search. Always use this to obtain information about current events.",
        ),
        Tool(
            name="ProductSearch",
            func=knowledge_base.run,
            description="Access to all our products. Always use this when asked about the products we offer",
        ),
    ]

    return tools