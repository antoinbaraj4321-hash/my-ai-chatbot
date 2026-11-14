
from flask import Flask, render_template, request, jsonify
import ollama
import sqlite3

app = Flask(__name__)

DB_NAME = "chat_history.db"
messages = []

# Database create
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT
            )
        """)

# Load saved messages
def load_history():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            "SELECT role, content FROM chat_history ORDER BY id"
        ).fetchall()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]

init_db()
messages = load_history()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["question"]

    messages.append({"role": "user", "content": question})

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO chat_history (role, content) VALUES (?, ?)",
            ("user", question)
        )

    response = ollama.chat(
        model="llama3.2:1b",
        messages=messages
    )

    answer = response.message.content

    messages.append({"role": "assistant", "content": answer})

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO chat_history (role, content) VALUES (?, ?)",
            ("assistant", answer)
        )

    return jsonify({"answer": answer})


@app.route("/history")
def history():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            "SELECT role, content FROM chat_history ORDER BY id"
        ).fetchall()

    return jsonify([
        {"role": role, "content": content}
        for role, content in rows
    ])

if __name__ == "__main__":
    app.run(debug=True)

