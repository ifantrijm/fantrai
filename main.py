from ollama import chat
import sqlite3

MODEL = "qwen2.5:3b"


def create_database():
    conn = sqlite3.connect("memory.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE If NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_memory(key, value):
    conn = sqlite3.connect("memory.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()


def get_memories():
    conn = sqlite3.connect("memory.db")

    cursor = conn.cursor()

    cursor.execute("SELECT key, value FROM memories")

    memories = cursor.fetchall()

    conn.close()

    return memories

create_database()

print("=" * 50)
print("              AiFan")
print("=" * 50)
print("AI Assistant pribadi Ifan")
print("Ketik 'exit' untuk keluar.\n")

while True:
    user_input = input("Prof: ")

    if user_input.lower() == "exit":
        print("AiFan: sampai jumpa")
        break

    memories = get_memories()

    memory_text = "\n".join(
        f"{key}: {value}"
        for key, value in memories
    )

    messages = [
        {
            "role": "system",
            "content": f"""
            kamu adalah AiFan, AI assistant pribadi milik Ifan.
            Gunakan informasi memory berikut jika relewan

            {memory_text}

            jawab menggunakan bahasi INdonesia yang santai dan mudah dipahami.

            """
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = chat(
        model=MODEL,
        messages=messages
    )

    answer = response.message.content

    print(f"AiFan: {answer}\n")