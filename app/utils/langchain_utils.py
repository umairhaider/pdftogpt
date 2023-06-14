import logging
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from app.api.knowledgebase_handler import get_knowledge_base, set_knowledge_base

# If the API key is not set, raise an exception
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    raise Exception("Please set your OPENAI_API_KEY as an environment variable.")

def process_file_context(file_text):
    try:
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(file_text)
        
        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        set_knowledge_base(knowledge_base)
    except Exception as e:
        logging.error(f"An error occurred during process_file_context(): {str(e)}")
        raise Exception(f"An error occurred during process_file_context(): {str(e)}")

def process_user_question(user_question):
    try:
        knowledge_base = get_knowledge_base()
        
        # show user input
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)

            return response
    except Exception as e:
        logging.error(f"An error occurred during process_user_question(): {str(e)}")
        raise Exception(f"An error occurred during process_user_question(): {str(e)}")