from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

template = """You are a chatbot having a conversation with a human.

Given the following extracted parts of a long document and a question, create a final answer.

{context}

{chat_history}
Human: {human_input}
Chatbot:"""

knowledge_base = None
memory = None
prompt = None

chunks = None

# Setup the context for the knowledge base
def set_app_context():
    global memory
    global prompt
    if not memory or not prompt:
        memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=10,
        return_messages=True,
        input_key="human_input")
        prompt = PromptTemplate(input_variables=["chat_history", "human_input", "context"], template=template)

# Reset the context for the knowledge base
def reset_app_context():
    global memory
    global prompt
    global knowledge_base
    memory = None
    prompt = None
    knowledge_base = None
    set_app_context()

# Getters and setters for the knowledge base
def get_memory():
    return memory

def get_prompt():
    return prompt

def get_knowledge_base():
    return knowledge_base

def get_chunks():
    return chunks

def set_chunks(new_chunks):
    global chunks
    chunks = new_chunks

def set_knowledge_base(new_context):
    global knowledge_base
    knowledge_base = new_context