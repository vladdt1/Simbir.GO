from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Опция для SQLAlchemy
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Замените на ваш секретный ключ

# Инициализация расширений
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Импорт и регистрация блюпринтов для контроллеров
from controllers.account_controller import account_blueprint
from controllers.transport_controller import transport_blueprint
from controllers.rent_controller import rent_blueprint
from controllers.payment_controller import payment_blueprint
from controllers.admin_account_controller import admin_account_blueprint
from controllers.admin_transport_controller import admin_transport_blueprint
from controllers.admin_rent_controller import admin_rent_blueprint

app.register_blueprint(account_blueprint)
app.register_blueprint(transport_blueprint)
app.register_blueprint(rent_blueprint)
app.register_blueprint(payment_blueprint)
app.register_blueprint(admin_account_blueprint)
app.register_blueprint(admin_transport_blueprint)
app.register_blueprint(admin_rent_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
