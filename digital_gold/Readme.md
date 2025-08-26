# 💰 Simplify Money - Digital Gold Investment Platform

This project is a **Digital Gold Investment workflow** built as part of the **Simplify Money Software Engineer Intern assignment**.  
It integrates an **LLM-powered AI assistant** with a **FastAPI backend** and **Streamlit frontend**, simulating digital gold purchases with database persistence.

---

## 🚀 Features
- **FastAPI Backend**
  - `/api/v1/llm-interaction` → AI-powered chat assistant
  - `/api/v1/purchase-gold` → Simulate digital gold purchase
  - `/api/v1/user/{id}/purchases` → User’s purchase history
  - `/api/v1/admin/stats` → Admin stats (total purchases, recent investments)

- **AI Assistant**
  - Powered by **Google Gemini API**
  - Gen-Z friendly tone with emojis
  - Educates, nudges, and encourages investments
  - Fallback responses if API unavailable

- **Database**
  - **SQLite** (`digital_gold.db`) for persistence
  - `users` and `gold_purchases` tables

- **Streamlit Frontend**
  - Conversational chat with AI assistant
  - One-click gold purchase simulation
  - Investment history dashboard
  - Quick stats and example queries

---

## 🛠️ Tech Stack
- **Backend**: FastAPI, Pydantic, SQLite
- **Frontend**: Streamlit
- **AI Integration**: Google Gemini API
- **Database**: SQLite
- **Testing**: FastAPI TestClient (`test_api.py`)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/<your-username>/Simplify_DigitalGoldInvestment.git
cd Simplify_DigitalGoldInvestment

2️⃣ Create Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3️⃣ Run the FastAPI Backend

uvicorn main:app --reload --host 127.0.0.1 --port 8000

4️⃣ Run the Streamlit Frontend

streamlit run app.py --server.port 8501

📂 Project Structure
.
├── main.py         # FastAPI backend
├── app.py          # Streamlit frontend
├── test_api.py     # API tests
├── digital_gold.db # SQLite database
└── README.md       # Documentation

🧪 Testing
pytest test_api.py

📝 Approach
Designed FastAPI backend for gold investment workflow with AI-powered advice.
Integrated Gemini API for conversational and contextual responses.
Used SQLite for persistence with tables for users and purchases.
Built Streamlit UI for:
Chat with AI assistant
Quick purchase flow
Investment history & stats
Implemented validations:
Min purchase: ₹10
Max purchase: ₹1,00,000
Added fallback AI responses if Gemini API is unavailable.

⚠️ Challenges & Future Improvements
Gemini API quota/availability → fallback responses used when API not available.
SQLite is lightweight, for production migrate to PostgreSQL/MySQL.
Authentication is basic → future scope: OAuth2 / JWT-based login.
Deployment tested locally → can be extended to Streamlit Cloud + Render/Railway.

👨‍💻 Author
Shrijan Sahu
