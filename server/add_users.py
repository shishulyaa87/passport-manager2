from models import db, User
from app import app
from werkzeug.security import generate_password_hash

def add_user(username, password):
    with app.app_context():
        if User.query.filter_by(username=username).first():
            print(f"Пользователь {username} уже существует")
            return
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"Пользователь {username} добавлен")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Использование: python add_user.py <username> <password>")
    else:
        add_user(sys.argv[1], sys.argv[2])
