### 📚 Library Management Microservice

A lightweight FastAPI-based microservice for managing books in a library system. Built using the MVC architecture with SQLite and SQLAlchemy. Designed to be modular and minimal.

---

### 🗂️ Project Structure

```
library_service/
├── app/
│   ├── controllers/      # FastAPI routes
│   ├── database/         # DB setup (SQLAlchemy + SQLite)
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic / DB queries
│   ├── utils/            # Utilities (e.g., hashing, helpers)
├── main.py               # FastAPI entry point
├── requirements.txt      # Python dependencies
└── Dockerfile            # For containerization
```

---

### 🚀 Features

- 📚 Create, read, update, and delete book records
- 📄 Swagger documentation available at `/docs`
- 🗃️ SQLite for lightweight local storage
- 🧼 Clean separation of concerns using MVC

---

### 🛠️ Running Locally

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Start Server

```bash
uvicorn main:app --reload
```

#### 3. Access API

- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root: [http://localhost:8000/library/books](http://localhost:8000/library/books)

---

### 🐳 Running with Docker

```bash
docker build -t library_service .
docker run -p 8000:8000 library_service
```

---

### 📌 Example API Endpoints

- `GET /library/books` – Get all books
- `POST /library/books` – Create a new book
- `GET /library/books/{id}` – Get book by ID
- `PUT /library/books/{id}` – Update book
- `DELETE /library/books/{id}` – Delete book

---
