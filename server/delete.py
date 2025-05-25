from models import db, User
from app import app

def delete_user(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"Пользователь {username} не найден")
            return
        db.session.delete(user)
        db.session.commit()
        print(f"Пользователь {username} удалён")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python delete_user.py <username>")
    else:
        delete_user(sys.argv[1])
