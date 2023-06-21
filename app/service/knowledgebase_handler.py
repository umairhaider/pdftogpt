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

def get_memory():
    return memory

def get_prompt():
    return prompt

def get_knowledge_base():
    return knowledge_base

def set_knowledge_base(new_context):
    global knowledge_base
    knowledge_base = new_context