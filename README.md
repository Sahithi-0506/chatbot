# 🤖 LangChain Gemini Chatbot

An AI-powered chatbot application built using LangChain, Google Gemini API, Python, and Streamlit.

This chatbot allows users to interact with an AI assistant through a simple web interface. The project demonstrates the integration of Large Language Models (LLMs) using the LangChain framework.

---

# 📌 Features

- Conversational AI chatbot
- Built using LangChain framework
- Google Gemini API integration
- Interactive Streamlit UI
- Environment variable security using `.env`
- Session-based chat memory
- Beginner-friendly project structure

---

# 🛠️ Technologies Used

- Python
- LangChain
- Google Gemini API
- Streamlit
- dotenv
- Git & GitHub

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

The application will run on:

```bash
http://localhost:8501
```

---

# 💡 How It Works

1. User enters a message in the chat interface.
2. LangChain processes the conversation.
3. Gemini API generates AI response.
4. Streamlit displays the conversation dynamically.

---

# 📸 Output Screenshot

![alt text](image.png)



# 🚀 Future Enhancements

- Add voice assistant support
- Store chat history in database
- Add multiple AI personalities
- Deploy using Streamlit Cloud
- Add authentication system

---

# 👩‍💻 Author

**Sahithi Achyutha Ishwarya Kalla**

- GitHub: https://github.com/Sahithi-0506
- LinkedIn: https://www.linkedin.com/in/sahithi-achyutha-ishwarya-kalla-317799319/
---

# 📄 License

This project is created for educational and learning purposes.