# Paramo_GPT

Here’s a polished and clear summary you can use in your project to explain **why you chose FAISS over Chroma**:

---

### 🧠 **Why We Chose FAISS Over Chroma for Our Group Project**

For our vector store, we chose **FAISS** instead of **Chroma** due to **cloud deployment compatibility and project scope**:

- **FAISS**, developed by **Meta (Facebook)**, is a **vector index library** designed for **efficient similarity search** on high-dimensional vectors (like embeddings).  
- It’s not a full vector database like Chroma, but it's **lightweight, fast, and ideal for in-memory use**.
- **Chroma**, on the other hand, depends on **SQLite ≥ 3.35.0**, which is **not supported on Streamlit Cloud**, leading to deployment errors.
- While Chroma is more suited for **production-level applications** with persistence and metadata, **FAISS is perfect for lightweight, local or cloud-compatible RAG applications**.
- Since our project is a **small-scale enterprise RAG prototype** with no need for persistent storage or cloud-scale database features, FAISS was the **most reliable and practical choice**.

✅ FAISS works smoothly on **Streamlit Cloud**  
❌ Chroma does not, due to **SQLite limitations**

---

Let me know if you'd like a visual or comparison table version too!