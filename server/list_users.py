from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'ID: {user.id}, Username: {user.username}')
