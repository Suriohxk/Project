# ♻️ Waste Wise — AI Waste Classification & Smart Disposal Assistant

> Aligned with **SDG 12 – Responsible Consumption and Production**
> Designed specifically for Indian households 🇮🇳

---

## 🗂 Project Structure

```
app/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── models/schemas.py        # Pydantic models
│   │   ├── routes/chat.py           # API endpoints
│   │   ├── nodes/graph.py           # LangGraph workflow
│   │   └── utils/
│   │       ├── classifier.py        # Keyword-based waste classifier
│   │       ├── webhook.py           # Webhook trigger
│   │       ├── supabase_client.py   # Supabase DB operations
│   │       └── session_store.py     # In-memory session store
│   ├── requirements.txt
│   ├── supabase_schema.sql
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── pages/ChatPage.jsx
    │   ├── components/
    │   │   ├── ChatBubble.jsx
    │   │   ├── ChatInput.jsx
    │   │   ├── WasteSummaryCard.jsx
    │   │   ├── EcoRewardBadge.jsx
    │   │   ├── ImageUpload.jsx
    │   │   └── TypingIndicator.jsx
    │   ├── hooks/useChat.js
    │   └── utils/api.js
    └── .env
```

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY, WEBHOOK_URL

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend runs at: **http://localhost:8000**
Swagger docs at: **http://localhost:8000/docs**

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 🗄 Supabase Setup

1. Create a free project at [supabase.com](https://supabase.com)
2. Open the SQL editor and run **`backend/supabase_schema.sql`**
3. Copy your project URL and anon key to `backend/.env`

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send a chat message |
| `POST` | `/api/chat/image` | Send a message with image |
| `GET`  | `/api/session/{id}` | Get session info & rewards |
| `DELETE` | `/api/session/{id}` | Reset session |
| `GET`  | `/health` | Health check |

### Sample API Request

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Rajan", "session_id": null}'
```

```bash
# Continue with age
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "25", "session_id": "<session_id_from_above>"}'
```

```bash
# Ask about waste
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "plastic bottle", "session_id": "<session_id>"}'
```

---

## 🧠 LangGraph Workflow

```
START
  │
  ▼
start_node         ← Greeting message
  │
  ▼
clarification_node ← Collect name → age → waste item (one at a time)
  │
  ├─ still collecting → END (wait for next message)
  │
  ▼
router_node        ← Classify waste via keyword matching
  │
  ├──► plastic_node   → Dry/Blue bin instructions
  ├──► organic_node   → Wet/Green bin + compost
  ├──► ewaste_node    → Authorized e-waste centers
  ├──► hazardous_node → Special disposal guidance
  └──► unknown_node   → General guidance
         │
         ▼
       final_node    ← Save to Supabase + trigger webhook
```

---

## ♻️ Waste Categories

| Category | Color | Examples | Points |
|----------|-------|----------|--------|
| Plastic  | 🔵 Blue | Plastic bottles, bags, wrappers | 10 |
| Organic  | 🟢 Green | Banana peel, rice, leaves | 8 |
| E-Waste  | 🟡 Amber | Old phone, laptop, cables | 15 |
| Hazardous | 🔴 Red | Batteries, paint, medicines | 20 |

---

## 🎁 Reward System

| Points | Level |
|--------|-------|
| 0–19   | 🌱 Beginner |
| 20–49  | ♻️ Eco Starter |
| 50–99  | 🌿 Green Hero |
| 100+   | 🏆 Eco Champion |

---

## 📦 Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS 3
- **Backend**: Python 3.11 + FastAPI
- **AI Workflow**: LangGraph (node-based state machine)
- **Database**: Supabase (PostgreSQL)
- **Webhook**: relay.app (configurable)

---

## 🌍 SDG 12 Alignment

This project directly supports **UN SDG Goal 12 – Responsible Consumption and Production** by:
- Educating Indian households on proper waste segregation
- Providing India-specific disposal guidance (Kabadiwala, municipal bins)
- Gamifying eco-friendly behavior with reward points
- Reducing contamination of recyclable materials
