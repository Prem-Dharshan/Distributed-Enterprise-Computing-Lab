## 📘 EverMicro — Gateway & Library Service

This is a lightweight FastAPI microservice setup including:

- 🧭 **Gateway Service** — central reverse proxy for all services.
- 📚 **Library Service** — simple book management API using SQLite.

Each service is **Dockerized**, but can also be run **standalone locally** for quick development and testing.

---

## 🗂 Project Structure

```
.
├── docker-compose.yml
├── gateway_service/
│   ├── app/
│   │   ├── controllers/
│   │   │   └── gateway_controller.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── library_service/
│   ├── app/
│   │   ├── controllers/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
```

---

## 🚀 Running via Docker Compose

### 🐳 Start All Services

```bash
docker-compose up --build
```

### ✅ Access Services

- Gateway API Docs: [http://localhost:8001/docs](http://localhost:8001/docs)
- Library API (via Gateway):  
  - `GET /api/library/books`  
  - `POST /api/library/books`  

---

## ⚙️ Running Services Individually (Dev Mode)

You can run each service standalone without Docker, great for local development.

---

### 📚 Run Library Service Locally

#### 1. Navigate

```bash
cd library_service
```

#### 2. Install Requirements

```bash
pip install -r requirements.txt
```

#### 3. Run the Server

```bash
uvicorn main:app --reload --port 8011
```

> 🟢 Visit: [http://localhost:8011/docs](http://localhost:8011/docs)

---

### 🧭 Run Gateway Service Locally

#### 1. Navigate

```bash
cd gateway_service
```

#### 2. Install Requirements

```bash
pip install -r requirements.txt
```

#### 3. Run the Server

```bash
uvicorn app.main:app --reload --port 8001
```

> 🔁 Ensure your `LIBRARY_SERVICE_URL` in `gateway_controller.py` points to:  
```python
LIBRARY_SERVICE_URL = "http://localhost:8011/library"
```

> ✅ Visit: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🔧 Notes

- Gateway forwards requests to the library service using a dynamic proxy route.
- Add more microservices like `auth`, `flight`, `weather`, etc., with similar `/api/<service>` forwarding in the gateway.
- No `.env` or config loaders — everything is hardcoded for simplicity.

---
