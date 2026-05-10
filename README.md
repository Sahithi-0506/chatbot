# 📚 AI Academic Study Assistant using RAG

An AI-powered Academic Study Assistant built using LangChain, Google Gemini API, Streamlit, and Retrieval-Augmented Generation (RAG).

This application allows students to upload subject PDFs, notes, or academic materials and ask questions based on the uploaded documents.

The chatbot retrieves relevant content from the uploaded PDF and generates contextual answers using Gemini AI.

---

# 🚀 Features

- 📄 Upload multiple academic PDF documents
- 🤖 AI-powered question answering
- 🔍 RAG (Retrieval-Augmented Generation) workflow
- 📚 Context-based answers from uploaded study materials
- 🧠 Semantic document retrieval
- ⚡ Gemini AI integration
- 💬 Interactive Streamlit user interface
- 🔐 Secure API key handling using `.env`

---

# 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini API
- RAG Architecture
- TF-IDF Retrieval
- PyPDF2
- scikit-learn
- dotenv

---

# 📂 Project Structure

```bash
langchain-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
```

---

# ⚙️ Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/langchain-chatbot.git
cd langchain-chatbot
```

## Step 2: Create Conda Environment

```bash
conda create -n langchain-env python=3.10 -y
conda activate langchain-env
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Configuration

Create a `.env` file in the project folder.

Add your Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

Application runs at:

```bash
http://localhost:8501
```

---

# 💡 How It Works

1. User uploads academic PDF documents.
2. PDF text is extracted and split into chunks.
3. Relevant chunks are retrieved using local similarity search.
4. Gemini AI generates answers using retrieved context.
5. Streamlit displays answers interactively.

---

# 📸 Output Screenshot

Add your project screenshot here.

```bash
![alt text](image-1.png)
```

---

# 🎯 Use Cases

- Exam preparation
- Quick revision
- Concept clarification
- Academic doubt solving
- Notes summarization

---

# 🚀 Future Enhancements

- Add chat history support
- Add voice assistant integration
- Add multi-subject organization
- Implement vector databases like FAISS
- Add authentication system
- Deploy advanced RAG pipeline

---

# 👩‍💻 Author

**Sahithi Achyutha Ishwarya Kalla**

- GitHub: https://github.com/Sahithi-0506
- LinkedIn: https://www.linkedin.com/in/sahithi-achyutha-ishwarya-kalla-317799319/

---

# 📄 License

This project is created for educational and learning purposes.