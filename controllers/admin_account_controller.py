from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Account, db
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_account_blueprint = Blueprint('admin_account', __name__)
admin_account_api = Api(admin_account_blueprint)

class AdminAccountResource(Resource):
    @jwt_required
    def get(self, id=None):
        # Получение информации об аккаунте (всех аккаунтах или по ID)
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        if id:
            account = Account.query.get(id)
            if not account:
                return {"message": "Account not found"}, 404

            return {
                "id": account.id,
                "username": account.username,
                "isAdmin": account.isAdmin,
                "balance": account.balance
            }

        start = request.args.get('start', default=0, type=int)
        count = request.args.get('count', default=10, type=int)
        accounts = Account.query.offset(start).limit(count).all()

        account_list = []
        for account in accounts:
            account_list.append({
                "id": account.id,
                "username": account.username,
                "isAdmin": account.isAdmin,
                "balance": account.balance
            })

        return {"accounts": account_list}

    @jwt_required
    def post(self):
        # Создание нового аккаунта администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        username = data['username']
        password = data['password']
        isAdmin = data['isAdmin']
        balance = data['balance']

        # Проверка наличия аккаунта с таким же именем пользователя
        existing_account = Account.query.filter_by(username=username).first()
        if existing_account:
            return {"message": "An account with this username already exists"}, 400

        # Создание нового аккаунта
        account = Account(username=username, password=password, isAdmin=isAdmin, balance=balance)
        db.session.add(account)
        db.session.commit()

        return {"message": "Account created successfully"}

    @jwt_required
    def put(self, id):
        # Изменение аккаунта администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        username = data['username']
        password = data['password']
        isAdmin = data['isAdmin']
        balance = data['balance']

        account = Account.query.get(id)
        if not account:
            return {"message": "Account not found"}, 404

        # Проверка наличия аккаунта с таким же именем пользователя, исключая текущий аккаунт
        existing_account = Account.query.filter(Account.id != id, Account.username == username).first()
        if existing_account:
            return {"message": "An account with this username already exists"}, 400

        account.username = username
        account.password = password
        account.isAdmin = isAdmin
        account.balance = balance
        db.session.commit()

        return {"message": "Account updated successfully"}

    @jwt_required
    def delete(self, id):
        # Удаление аккаунта администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        account = Account.query.get(id)
        if not account:
            return {"message": "Account not found"}, 404

        db.session.delete(account)
        db.session.commit()

        return {"message": "Account deleted successfully"}

admin_account_api.add_resource(AdminAccountResource, '/api/Admin/Account', '/api/Admin/Account/<int:id>')
