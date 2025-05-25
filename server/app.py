from flask import Flask
from flask_cors import CORS
import os
import logging

# Включаем логирование
logging.basicConfig(level=logging.DEBUG)

# Инициализация Flask-приложения
app = Flask(__name__)
CORS(app)

# Конфигурация базы данных SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

from routes import init_routes
init_routes(app)

@app.route('/')
def index():
    return {"message": "Сервер работает"}

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Exception: {e}")
    return {"message": "Internal Server Error"}, 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
