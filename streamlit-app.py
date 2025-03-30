#0. Importing the necessary libraries
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


#1. Loading Google API key from st.secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Defining safe path to local PDF (in the same folder as this file)
current_dir = os.path.dirname(__file__)
pdf_filename = "PAGOS 20 MARZO.pdf"
pdf_path = os.path.join(current_dir, pdf_filename)

st.title("📄 Paramo GPT - Ask Any Question About Paramo Payments To Suppliers")

# --- LOAD & PROCESS PDF --- #

try:
    # Load the local PDF
    loader = PyPDFLoader(pdf_path)
    raw_docs = loader.load()

    # Split document into chunks
    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    split_docs = splitter.split_documents(raw_docs)

    # Embeddings model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create FAISS vector store in-memory --> We used FAISS over Chroma because it is the best option for cloud compatibility
    db = FAISS.from_documents(split_docs, embedding)
    retriever = db.as_retriever()

    # --- RAG Chain Setup --- #

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:

    {context}

    Question: {question}
    """)

    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # --- Streamlit UI --- #

    user_input = st.text_input("💬 Ask something about the PDF")

    if user_input:
        with st.spinner("Thinking..."):
            response = chain.invoke(user_input)
        st.markdown("### ✅ Answer:")
        st.write(response)

except Exception as e:
    st.error(f"⚠️ Error loading or processing the PDF: {e}")
