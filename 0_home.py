#0. Importing the necessary libraries
import os


#1. Loading Google API key from st.secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Defining safe path to local PDF (in the same folder as this file)
current_dir = os.path.dirname(__file__)
pdf_filename = "PAGOS 20 MARZO.pdf"
pdf_path = os.path.join(current_dir, pdf_filename)

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
    st.image('logoparamonegro.png', width=200)
    st.markdown("---")
    st.title("Páramo GPT")


    st.markdown("""### What is Páramo GPT and why is it valuable?

**Páramo GPT** is an enterprise-level **Retrieval-Augmented Generation (RAG)** application designed to enhance how the company interacts with its supplier payment data. Instead of manually searching through large PDFs, users can simply ask natural-language questions and get instant, accurate answers.

By integrating AI with Páramo’s existing workflows, this tool delivers:

- ✅ **Faster access to payment information**
- ✅ **Reduced errors when verifying transactions**
- ✅ **Time savings for audits, reports, and support**
- ✅ **Scalable insights as data volume grows**

In short, **Páramo GPT transforms raw financial documents into actionable insights**, boosting transparency and operational efficiency across the organization.""")

    st.markdown("---")

    user_input = st.text_input("💬 Ask any question about payments to suppliers")

    if user_input:
        with st.spinner("Thinking..."):
            response = chain.invoke(user_input)
        st.markdown("### ✅ Answer:")
        st.write(response)



except Exception as e:
    st.error(f"⚠️ Error loading or processing the PDF: {e}")