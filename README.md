# 🤖 AI Chatbot Backend

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![APScheduler](https://img.shields.io/badge/APScheduler-Background%20Tasks-orange?style=for-the-badge)

Welcome to the **AI Chatbot Backend** project! This is a high-performance, asynchronous REST API built with **FastAPI** designed to power intelligent conversational interfaces. 

This project demonstrates a production-ready architecture for handling **User Authentication**, **Retrieval-Augmented Generation (RAG)**, and **Persistent Chat History**, showcasing modern backend development practices.

---

## 🚀 Key Features

* **🔐 User Authentication:** Secure Signup & Login utilizing JWT (JSON Web Tokens) and Bcrypt password hashing.
* **🧠 RAG Pipeline:** Context-aware responses using a knowledge base with intelligent keyword optimization (Stop-word filtering).
* **💾 Persistent Memory:** Stores user conversations and AI responses in **PostgreSQL**.
* **⚡ High Performance:** Built on **FastAPI** for asynchronous request handling (ideal for AI/ML workloads).
* **🕰️ Background Tasks:**
    * Daily automated cleanup of chat history older than 30 days.
    * Asynchronous email verification simulation upon user signup.
* **📑 API Documentation:** Interactive Swagger UI & ReDoc integrated.

---

## 🛠️ Tech Stack & Design Decisions

Here is a breakdown of the technologies used and the rationale behind them:

| Component | Technology | Why I Chose This? |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | Chosen over Django/Flask for its **native async support** (crucial for AI latency), automatic validation (Pydantic), and superior performance. |
| **Database** | **PostgreSQL** | Selected for its **ACID compliance** and relational integrity, ensuring data consistency for user accounts and chat logs. |
| **ORM** | **SQLAlchemy** | Provides a powerful abstraction layer for database interactions and migration management. |
| **Auth** | **JWT + Passlib** | Stateless authentication ensures scalability, while `bcrypt` ensures password security at rest. |
| **Scheduling** | **APScheduler** | A robust solution for handling periodic maintenance tasks without blocking the main application thread. |

---

## 📂 Project Structure

```bash
AI-Chatbot-Backend/
├── backend/
│   ├── apis/v1/            # API Routes (Auth, Chat)
│   ├── core/               # Configuration (Env vars, Security)
│   ├── data/               # Knowledge Base (JSON source for RAG)
│   ├── db/                 # Database Connection & Models
│   ├── schemas/            # Pydantic Data Validation Models
│   ├── services/           # Business Logic (RAG Service, Background Tasks)
│   └── main.py             # App Entry Point & Lifespan Events
├── .env                    # Environment Variables
├── pyproject.toml          # Dependency Management
└── README.md               # Documentation
```

---

1. **User Query:** User asks a question via the protected `/chat` endpoint.
2. **Context Retrieval:** The system extracts keywords and searches `knowledge.json` for the most relevant match using a weighted scoring algorithm.
3. **Augmentation:** The retrieved context is prepended to the user query.
4. **Response Generation:** The final response is generated based strictly on the retrieved facts to prevent hallucinations.

---

## 📸 API Demonstration (Preview)

Below is a preview of the **Swagger UI** and a sample **RAG-based conversation** from the actual application:

### 1. Interactive Documentation (Swagger UI)
<img width="1000" height="600" alt="swaggerUI" src="https://github.com/user-attachments/assets/0e1cfdb9-d7af-42bd-98f6-8c97eb120989" />

### 2. Sample RAG Conversation
**Endpoint:** `POST /api/v1/chat/chat`  
**Scenario:** User asking about the payment process.

**Request:**
```json
{
  "message": "What is your payment process?"
}
```

**Response:**

```json
{
  "response": "🔍 **Retrieved Context:** We accept all major credit cards including Visa, MasterCard... 🤖 **AI Answer:** Based on our documents, we accept multiple payment methods including Visa, MasterCard, and PayPal."
}

```

## 🏗️ Technical Architecture (Deep Dive)

### 1. The RAG Pipeline (Retrieval-Augmented Generation)
Instead of relying solely on an LLM's training data, this system uses a **Knowledge Base (`knowledge.json`)** to provide accurate, domain-specific answers.
* **Retrieval Logic:** When a user queries, the system first filters out "stop words" (e.g., *is, the, are*) to extract core keywords. It then scans the knowledge base for matching topics or content.
* **Generation:** If a document is found, it is injected into the AI's context window. If not, a graceful fallback mechanism is triggered to prevent hallucinations.

### 2. Database Schema Design
I implemented a **Relational Model (One-to-Many)** to efficiently manage data:
* **`User` Model:** Stores credentials (`email`, `hashed_password`).
* **`ChatHistory` Model:** Stores `message`, `is_user_message` (bool), and `timestamp`.
* **Relationship:** A Foreign Key (`user_id`) links chats to specific users. This ensures data isolation—users can only access their own history.

### 3. Security Measures
* **Password Hashing:** Passwords are salted and hashed using `bcrypt` before storage.
* **Token Security:** API endpoints are protected via `OAuth2PasswordBearer`. Every request header is validated for a legitimate, non-expired JWT signature.

### 4. Background Task Management
To keep the API response time low:
* **Email Verification:** Triggered via FastAPI's `BackgroundTasks` immediately after signup. This allows the API to return a "Success" response instantly while the email sends in the background.
* **Data Cleanup:** An `APScheduler` job runs every 24 hours to identify and delete chat records older than 30 days, keeping the database optimized.

---

## ⚙️ Setup & Installation

Follow these steps to run the project locally:

### Prerequisites
* Python 3.10+
* PostgreSQL (Local or Cloud like Neon/Supabase)

### 1. Clone the Repository
```bash
git clone https://github.com/mdwasikhan54/AI-Chatbot-Backend.git
cd AI-Chatbot-Backend
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your credentials:
```ini
PROJECT_NAME="AI Chatbot"
PROJECT_VERSION="1.0.0"
DATABASE_URL="postgresql://user:password@localhost/dbname"
SECRET_KEY="your_super_secret_key_change_this"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY="your_openai_key_or_mock"
```

### 3. Install Dependencies
Using **Poetry** (Recommended):
```bash
poetry install
```
Or using **pip**:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt apscheduler python-dotenv requests multipart
```

### 4. Run the Application
```bash
uvicorn backend.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## 📖 API Documentation

The API comes with auto-generated interactive documentation.

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Core Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/signup` | Register new user & trigger verification email |
| `POST` | `/api/v1/auth/login` | Authenticate & receive Access Token |
| `POST` | `/api/v1/chat/chat` | Send message to AI (Requires Auth) |
| `GET` | `/api/v1/chat/chat-history` | Retrieve user conversation history |
| `DELETE` | `/api/v1/chat/chat-history` | Clear personal chat history |

---

## 🔮 Future Improvements

If I were to expand this project further, I would implement:
* **Vector Database (Pinecone/FAISS):** To replace keyword search with semantic search for better context understanding.
* **WebSockets:** For real-time, bi-directional streaming of AI responses.
* **Redis Caching:** To cache frequent queries and reduce database load.

---

### 👨‍💻 Developed by [MD WASI KHAN](https://mdwasikhan-portfolio.netlify.app/) 

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdwasikhan54)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mdwasikhan54)
</div>

If you find this project helpful, please drop a ⭐ star on the repo\!

