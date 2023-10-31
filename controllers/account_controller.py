from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Account, db
from flask_jwt_extended import jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

account_blueprint = Blueprint('account', __name__)
account_api = Api(account_blueprint)

class AccountMeResource(Resource):
    @jwt_required
    def get(self):
        # Получение данных о текущем аккаунте
        current_user_id = current_user.id
        account = Account.query.get(current_user_id)

        if not account:
            return {"message": "Account not found"}, 404

        return {
            "id": account.id,
            "username": account.username,
            "isAdmin": account.isAdmin,
            "balance": account.balance
        }

class AccountSignInResource(Resource):
    def post(self):
        # Вход пользователя и генерация нового JWT токена
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        account = Account.query.filter_by(username=username).first()

        if not account or not check_password_hash(account.password, password):
            return {"message": "Invalid credentials"}, 401

        access_token = account.generate_access_token()
        return {"access_token": access_token}

class AccountSignUpResource(Resource):
    def post(self):
        # Регистрация нового аккаунта
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        existing_account = Account.query.filter_by(username=username).first()
        if existing_account:
            return {"message": "An account with this username already exists"}, 400

        hashed_password = generate_password_hash(password, method='sha256')

        account = Account(username=username, password=hashed_password, isAdmin=False, balance=0.0)
        db.session.add(account)
        db.session.commit()

        access_token = account.generate_access_token()
        return {"access_token": access_token}

class AccountSignOutResource(Resource):
    @jwt_required
    def post(self):
        # Выход из аккаунта
        # Для JWT, обычно, нет необходимости в явном выходе, так как токен самоуничтожается после истечения срока действия
        return {"message": "Sign out successful"}

class AccountUpdateResource(Resource):
    @jwt_required
    def put(self):
        # Обновление своего аккаунта
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        current_user_id = current_user.id
        account = Account.query.get(current_user_id)

        if not account:
            return {"message": "Account not found"}, 404

        # Проверка наличия аккаунта с таким же именем пользователя, исключая текущий аккаунт
        existing_account = Account.query.filter(Account.id != current_user_id, Account.username == username).first()
        if existing_account:
            return {"message": "An account with this username already exists"}, 400

        account.username = username
        account.password = generate_password_hash(password, method='sha256')
        db.session.commit()

        return {"message": "Account updated successfully"}

account_api.add_resource(AccountMeResource, '/api/Account/Me')
account_api.add_resource(AccountSignInResource, '/api/Account/SignIn')
account_api.add_resource(AccountSignUpResource, '/api/Account/SignUp')
account_api.add_resource(AccountSignOutResource, '/api/Account/SignOut')
account_api.add_resource(AccountUpdateResource, '/api/Account/Update')
