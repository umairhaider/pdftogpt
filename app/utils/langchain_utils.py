import logging
import os
import openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from app.service.knowledgebase_handler import get_knowledge_base, set_knowledge_base, set_app_context, get_memory, get_prompt

# Configure OpenAI API credentials
def set_openai_key():
    openai.api_key = os.getenv("OPENAI_API_KEY")

# If the API key is not set, raise an exception
if openai.api_key is None:
    raise Exception("Please set your OPENAI_API_KEY as an environment variable.")

# Setup the context for the knowledge base
set_app_context()


def process_file_context(file_text):
    try:
        set_openai_key()
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
        set_openai_key()
        knowledge_base = get_knowledge_base()
        
        # show user input
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            
            llm = OpenAI(temperature=0, max_tokens=100)
            chain = load_qa_chain(llm, chain_type="stuff", memory=get_memory(), prompt=get_prompt())
            with get_openai_callback() as cb:
                response = chain({"input_documents": docs, "human_input": user_question}, return_only_outputs=True)
                print(cb)

            return response
    except Exception as e:
        logging.error(f"An error occurred during process_user_question(): {str(e)}")
        raise Exception(f"An error occurred during process_user_question(): {str(e)}")