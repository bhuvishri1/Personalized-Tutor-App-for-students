import streamlit as st
from PyPDF2 import PdfReader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from streamlit_chat import message
import time
import os

st.title(":white[DocuChat: Chat with Pdf]")
st.header("Engage in Dynamic PDF Conversations",divider='rainbow')

st.markdown("""Are you tired of the traditional way of extracting information from your documents? Say hello to DocuChat, your interactive PDF companion! With DocuChat, you can effortlessly converse with your PDFs, making information retrieval an engaging and intuitive experience.""")

st.subheader("How it Works?")

st.markdown(""" 1)Upload Your PDF: Select a PDF document of your choice.
2) Chat with Your Document: Once uploaded, you can initiate a conversation with your PDF. Ask questions, seek information, and explore the content in a conversational manner.
3) Real-Time Responses: DocuChat leverages advanced language models to understand your queries and provide real-time responses. No more tedious scrolling or searching! """)

st.subheader("Use cases:")

st.markdown(""" 1) Study Aid: Quickly find relevant information for your research or studies.
2) Document Understanding: Easily comprehend complex documents through interactive conversations.
3) QA Sessions: Conduct question and answer sessions with your PDFs for enhanced comprehension. """)


os.environ["OPENAI_API_KEY"] = " "

def Text_extractor(uploaded_files1):
        reader_report = PdfReader(uploaded_files1)
        raw_text = ''
        for i, page in enumerate(reader_report.pages):
            text = page.extract_text()
            if text:
                raw_text += text 
        return raw_text
        
    
def initialize_embeddings_and_vector_store(texts):
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    # chunk_overlap  = 200,
    length_function = len,
    )
    texts_1 = text_splitter.split_text(texts)
    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts_1, embeddings)
    return embeddings, docsearch

# Initialize the QA chain
chain = load_qa_chain(OpenAI(), chain_type="stuff")
# Use st.session_state to store state across reruns
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None

if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None

if 'docsearch' not in st.session_state:
    st.session_state.docsearch = None

if 'history' not in st.session_state:
    st.session_state.history = []

uploaded_files1 = st.file_uploader("Choose a Pdf file ")
if uploaded_files1 and st.session_state.extracted_text is None:
    st.session_state.extracted_text = Text_extractor(uploaded_files1)
    st.write("Your data is extracted")

# Initialize embeddings and vector store
if st.session_state.extracted_text and (st.session_state.embeddings is None or st.session_state.docsearch is None):
    st.session_state.embeddings, st.session_state.docsearch = initialize_embeddings_and_vector_store(st.session_state.extracted_text)


# Initialize chat history
if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
         st.markdown(message["content"])

        # Accept user input
if prompt := st.chat_input("Query the pdf"):
        # Add user message to chat history
        
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
         st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response=""

            # Retrieve relevant documents based on conversation history
            conversation_history =  "".join([message["content"] for message in st.session_state.history])
            docs = st.session_state.docsearch.similarity_search(conversation_history)

            # Include conversation history in the question
            assistant_response=chain.run(input_documents=docs, question=conversation_history)

            # Add assistant message to conversation history
            st.session_state.history.append({"role": "assistant", "content": assistant_response})

            for chunk in assistant_response.split():
               full_response += chunk + " "
               time.sleep(0.05)
               # Add a blinking cursor to simulate typing
               message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response })

  
