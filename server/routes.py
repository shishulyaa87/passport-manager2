from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, PasswordEntry
from encryption import encrypt_password, decrypt_password  # исправлено имена функций
import logging

logger = logging.getLogger(__name__)
routes_bp = Blueprint('routes_bp', __name__, url_prefix='/api')

@routes_bp.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@routes_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Введите логин и пароль'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Пользователь уже существует'}), 409

    # Хэшируем пароль пользователя (без шифрования)
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Пользователь зарегистрирован'}), 201
    except Exception as e:
        logger.error(f"Ошибка регистрации: {e}")
        db.session.rollback()
        return jsonify({'message': 'Ошибка сервера'}), 500

@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Неверный логин или пароль'}), 401

    return jsonify({'message': 'Вход выполнен успешно'}), 200

@routes_bp.route('/passwords/<username>', methods=['GET'])
def get_passwords(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404

    entries = PasswordEntry.query.filter_by(user_id=user.id).all()
    # Расшифровываем пароли перед отправкой
    result = []
    for entry in entries:
        decrypted_password = decrypt_password(entry.password)
        result.append({
            'id': entry.id,
            'service': entry.service,
            'login': entry.login,
            'password': decrypted_password
        })

    return jsonify(result), 200

@routes_bp.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json(force=True)
    username = data.get('username')
    service = data.get('service')
    login = data.get('login')
    password = data.get('password')

    if not all([username, service, login, password]):
        return jsonify({'message': 'Недостаточно данных'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404

    existing = PasswordEntry.query.filter_by(user_id=user.id, service=service, login=login).first()
    if existing:
        return jsonify({'message': 'Запись уже существует'}), 409

    try:
        # Шифруем пароль перед сохранением
        encrypted_password = encrypt_password(password)
        new_entry = PasswordEntry(user_id=user.id, service=service, login=login, password=encrypted_password)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Пароль успешно добавлен'}), 201
    except Exception as e:
        logger.error(f"Ошибка при добавлении пароля: {e}")
        db.session.rollback()
        return jsonify({'message': 'Ошибка сервера'}), 500

@routes_bp.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json(force=True)
    username = data.get('username')
    old_service = data.get('old_service')
    old_login = data.get('old_login')
    new_service = data.get('new_service')
    new_login = data.get('new_login')
    new_password = data.get('new_password')

    if not all([username, old_service, old_login, new_service, new_login, new_password]):
        return jsonify({'message': 'Недостаточно данных'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404

    entry = PasswordEntry.query.filter_by(user_id=user.id, service=old_service, login=old_login).first()
    if not entry:
        return jsonify({'message': 'Запись не найдена'}), 404

    entry.service = new_service
    entry.login = new_login
    # Шифруем новый пароль перед сохранением
    entry.password = encrypt_password(new_password)

    try:
        db.session.commit()
        return jsonify({'message': 'Пароль обновлён'}), 200
    except Exception as e:
        logger.error(f"Ошибка при обновлении: {e}")
        db.session.rollback()
        return jsonify({'message': 'Ошибка сервера'}), 500

@routes_bp.route('/delete_password', methods=['POST'])
def delete_password():
    data = request.get_json(force=True)
    username = data.get('username')
    service = data.get('service')
    login = data.get('login')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404

    entry = PasswordEntry.query.filter_by(user_id=user.id, service=service, login=login).first()
    if not entry:
        return jsonify({'message': 'Запись не найдена'}), 404

    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Пароль удалён'}), 200
    except Exception as e:
        logger.error(f"Ошибка удаления: {e}")
        db.session.rollback()
        return jsonify({'message': 'Ошибка сервера'}), 500

def init_routes(app):
    app.register_blueprint(routes_bp)
