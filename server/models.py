from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(120), nullable=False)       # название сервиса (например, Gmail)
    login = db.Column(db.String(120), nullable=False)         # логин/почта для сервиса
    password = db.Column(db.String(120), nullable=False)      # сохранённый пароль (зашифрованный/хэш или как будет)
    user = db.relationship('User', backref=db.backref('passwords', lazy=True))
