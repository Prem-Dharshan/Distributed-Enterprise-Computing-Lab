## 📡 Notification Microservice

A lightweight, real-time WebSocket-based service that allows clients to subscribe to **multiple broadcast channels** like `sp-news`, `et-memes`, etc. Channels follow the `ab-ab` naming convention.

---

### ✅ Features

- 🔌 Real-time broadcasting using WebSockets
- 🧑 Clients can subscribe and **switch channels** on the fly
- 🔍 REST API to **search available channels** (`GET /channels?q=sp`)
- 📂 Fully modular with clean separation of concerns
- 🐳 Dockerized for easy integration

---

### 📁 Folder Structure

```
notification_service/
├── app/
│   ├── core/
│   │   ├── channel_manager.py  # Manages all channels and sockets
│   │   └── types.py            # Shared types
│   ├── routers/
│   │   └── channels.py         # Search API
│   └── main.py                 # FastAPI App & WebSocket Handler
├── requirements.txt
├── Dockerfile
└── README.md
```

---

### 🚀 How to Run (Locally)

#### 1. Install dependencies

```bash
pip install -r requirements.txt
```

#### 2. Start the server

```bash
uvicorn app.main:app --reload --port 8004
```

#### 3. Access WebSocket

Connect using your client (frontend or tool like [websocat](https://github.com/vi/websocat)):

```bash
ws://localhost:8004/ws/sp-news
```

#### 4. Search Channels

```http
GET http://localhost:8004/channels?q=sp
```

