# 📚 Library Manager

A simple full-stack library management app built with a **Flask REST API** and a **Vue 3 frontend**. It lets you add, browse, search, filter, and remove books, with all data persisted to a local JSON file.

---

## Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Backend  | Python 3, Flask, flask-cors |
| Frontend | Vue 3, TypeScript, Vite |
| Storage  | JSON file (`books.json`) |

---

## Project Structure

```
library-manager/
│
├── library-backend/
│   ├── api.py            # Flask REST API
│   ├── library.py        # Book & Library classes + JSON persistence
│   └── books.json        # Auto-generated on first book added
│
├── library-ui/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── BookManager.vue   # Main UI component
│   │   └── ...
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── README.md
│
├── .gitignore
└── README.md             # You are here
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+

---

### 1. Backend (Flask API)

```bash
# Install dependencies
pip install flask flask-cors

# Start the API server
python api.py
```

The API will be running at `http://localhost:5000`.

#### Endpoints

| Method | Endpoint          | Description         |
|--------|-------------------|---------------------|
| GET    | `/`               | Health check        |
| GET    | `/books`          | List all books      |
| POST   | `/books`          | Add a new book      |
| DELETE | `/books/<title>`  | Remove a book       |

---

### 2. Frontend (Vue 3)

```bash
cd library-ui

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be running at `http://localhost:5173`.

---

## Features

- Add books with title, author, ISBN, and page count
- Remove books from the library
- Search by title, author, or ISBN
- Filter by availability (All / Available / Borrowed)
- Live book count — *Showing X of Y books*
- Data persists across sessions via `books.json`
- Graceful fallback to sample data if the API is unreachable