import sqlite3
import bcrypt

DB_NAME = 'passwords.db'

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as conn:
        c = conn.cursor()

        # Таблица пользователей
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        # Таблица паролей
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                site TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()

# --------- Пользователи ---------
def register_user(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        with get_db() as conn:
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            return True, "Пользователь успешно зарегистрирован"
    except sqlite3.IntegrityError:
        return False, "Пользователь с таким именем уже существует"

def authenticate_user(username, password):
    with get_db() as conn:
        cur = conn.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and bcrypt.checkpw(password.encode(), row[1]):
            return True, row[0]  # Возвращаем user_id
        return False, None

def get_user_id(username):
    with get_db() as conn:
        cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        return row[0] if row else None

# --------- Пароли ---------
def save_password(user_id, site, login, password):
    with get_db() as conn:
        conn.execute("INSERT INTO passwords (user_id, site, login, password) VALUES (?, ?, ?, ?)",
                     (user_id, site, login, password))
        conn.commit()

def get_passwords(user_id):
    with get_db() as conn:
        cur = conn.execute("SELECT id, site, login, password FROM passwords WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def delete_password(password_id):
    with get_db() as conn:
        conn.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
        conn.commit()
