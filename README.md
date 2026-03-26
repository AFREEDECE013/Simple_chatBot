# 💬 Gemini Chatbot (Streamlit)

A simple and scalable AI chatbot built using **Streamlit** and the latest **Google Gemini (`google-genai`) SDK**.
This app supports conversational AI and can be extended with database storage, analytics, and more.

---

## 🚀 Features

* 🤖 Powered by Gemini AI (`gemini-2.5-flash`)
* 💬 Chat-style UI using Streamlit
* 🔐 Secure API key management using `.env`
* 🧠 Chat history (session-based / extendable to DB)
* ⚡ Fast and lightweight

---

## 📁 Project Structure

```
chatbot/
│
├── chatbot.py                # Main Streamlit app
├── check_available_models.py # Script to list available models
├── .env                      # API key (ignored in Git)
├── .gitignore                # Ignore sensitive files
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Requirements

Create a `requirements.txt` file with the following:

```
streamlit
google-genai
python-dotenv
```

---

## 🔑 Setup Instructions

### 1️⃣ Clone the Repository

```
git clone <your-repo-url>
cd chatbot
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file in the root folder:

```
GOOGLE_API_KEY=your_api_key_here
```

> ⚠️ Never commit this file. It is already added to `.gitignore`.

---

## ▶️ Run the Application

```
python -m streamlit run .\chatbot.py
```

App will open in your browser:

```
http://localhost:8501
```

---

## 🧠 How It Works

1. User enters a message
2. Message is sent to Gemini API
3. Response is generated using:

   ```
   gemini-1.5-flash
   ```
4. Chat is displayed in real-time

---

## 🔄 Check Available Models

Run this script:

```
python check_available_models.py
```

---

## 🔐 Security Best Practices

* ✅ Use `.env` for API keys
* ✅ Add `.env` to `.gitignore`
* ❌ Never push API keys to GitHub
* 🔁 Regenerate key if exposed

---

## 🚀 Future Improvements

* 💾 Store chat history in SQLite / PostgreSQL
* 👤 Multi-user authentication
* 📊 Dashboard for analytics
* 🔎 Connect with Ads / DV360 data
* ☁️ Deploy on Streamlit Cloud / GCP

---

## 🛠️ Troubleshooting

### ❌ Model Not Found Error

* Ensure you're using:

  ```
  gemini-2.5-flash
  ```
* Update package:

  ```
  pip install --upgrade google-genai
  ```

---

### ❌ API Key Issues

* Check `.env` file
* Ensure key is valid and active

---

## 📌 Command Summary

```
pip install -r requirements.txt
python -m streamlit run .\chatbot.py
```

---

## 👨‍💻 Author

**Afreed Beig**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

## used this as a reference
# https://www.geeksforgeeks.org/python/simple-chatbot-application-using-python-googleapikey/