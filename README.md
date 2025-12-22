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

## ❓ Implementation Q&A

### 1. How did you integrate the RAG pipeline for the chatbot, and what role does document retrieval play in the response generation?
I integrated the RAG pipeline within the `ChatService` class (`rag_service.py`).
* **Integration:** The system loads a structured `knowledge.json` file on startup. When a user sends a query, the system first filters out stop words (e.g., *is, the, are*) to extract core keywords. It then scans the knowledge base for matching topics or content content using a keyword search algorithm.
* **Role of Retrieval:** Document retrieval acts as the "Grounding" mechanism. Instead of relying solely on the AI model's training data (which can hallucinate), the retrieved document snippet provides the factual context. This context is injected into the prompt (*"Based on [Context], answer [Query]"*), ensuring the AI's response is accurate and domain-specific.

### 2. What database and model structure did you use for storing user and chat history, and why did you choose this approach?
I utilized a **Relational Database (PostgreSQL)** with **SQLAlchemy ORM**.
* **Structure:**
    * **`User` Model:** Stores `email`, `hashed_password`, and `is_active` status.
    * **`ChatHistory` Model:** Stores `message`, `is_user_message` (boolean), `timestamp`, and a Foreign Key `user_id`.
* **Why this approach?** I chose a relational model (One-to-Many) because chat history is inherently structured and must be strictly linked to specific users. PostgreSQL ensures data integrity (ACID compliance) and allows for efficient querying of historical data indexed by user IDs, which is more reliable than NoSQL for this specific schema.

### 3. How did you implement user authentication using JWT? What security measures did you take for handling passwords and tokens?
Authentication is handled via the `route_auth.py` module using the **OAuth2** standard with **JWT (JSON Web Tokens)**.
* **Implementation:** Upon valid login, the server issues a signed JWT containing the user's email (`sub`) and an expiration time (`exp`).
* **Security Measures:**
    * **Password Hashing:** Passwords are never stored in plain text. I used `bcrypt` (via `passlib`) for strong hashing and salting before storage.
    * **Token Validation:** Protected routes use `OAuth2PasswordBearer`. A custom dependency (`get_current_user`) verifies the JWT signature on every request to ensure it hasn't been tampered with or expired.

### 4. How does the chatbot generate responses using the AI model (GPT-3) after retrieving documents?
The response generation logic is orchestrated in the `get_response` method:
1.  **Context Retrieval:** The system searches the knowledge base for relevant information based on the user's query.
2.  **Prompt Engineering:** If a relevant document is found, it constructs a prompt that combines the retrieved context with the user's question.
3.  **Generation:** This structured prompt is passed to the AI model logic. (Note: For this submission, the OpenAI API call is architecturally mocked to simulate the behavior without incurring costs/latency, returning a formatted response that cites the retrieved context).
4.  **Fallback:** If no documents match, a fallback mechanism triggers a polite response indicating that information is unavailable, preventing false answers.

### 5. How did you schedule and implement background tasks for cleaning up old chat history, and how often do these tasks run?
I implemented background tasks using the **APScheduler** library for precision and **FastAPI BackgroundTasks** for immediate actions.
* **Cleanup Task:** A background job (`delete_old_chat_history`) is scheduled to run **every 24 hours** (Daily). It executes a database query to delete `ChatHistory` records where the timestamp is older than 30 days.
* **Email Task:** For the "Welcome Email" feature, I used FastAPI's native `BackgroundTasks`. This allows the email sending function to run asynchronously *after* the HTTP response is returned to the user, ensuring the signup API remains fast and non-blocking.

### 6. What testing strategies did you use to ensure the functionality of the chatbot, authentication, and background tasks?
* **Interactive API Testing:** I extensively used the **Swagger UI** (`/docs`) to manually test user flows: registering a new user, logging in to get a token, and using that token to access the protected `/chat` endpoint.
* **Edge Case Validation:** I tested specific scenarios such as:
    * Queries with no matching documents (to verify fallback logic).
    * Invalid or expired tokens (to verify security gates).
    * Duplicate email registration (to verify database constraints).
* **Latency Monitoring:** I observed response times during the RAG process to ensure the async pipeline performs within acceptable limits.

### 7. What external services (APIs, databases, search engines) did you integrate, and how did you set up and configure them?
* **Database:** Integrated **Neon DB** (Serverless PostgreSQL) via connection string configuration.
* **AI Service:** The architecture is designed for **OpenAI API** integration.
* **Configuration:** All external service credentials (Database URL, API Keys, Secret Keys) are managed securely via a `.env` file using `pydantic-settings`. This ensures sensitive data is decoupled from the codebase and easy to configure across environments.

### 8. How would you expand this chatbot to support more advanced features, such as real-time knowledge base updates or multi-user chat sessions?
* **Real-time Updates:** I would implement an Admin API endpoint (e.g., `POST /knowledge/upload`) that allows uploading PDF or Text files. These would be parsed and indexed into the knowledge base dynamically without requiring a server restart.
* **Vector Database:** To support more advanced retrieval, I would migrate from keyword search to a Vector Database (like **Pinecone** or **FAISS**) to enable semantic search.
* **Multi-user Sessions:** The current database schema already supports multi-user sessions via `user_id`. To enhance this, I would integrate **WebSockets** to support real-time, bi-directional streaming of chat messages for a more fluid user experience.

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
