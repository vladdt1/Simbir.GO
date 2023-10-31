from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0.0)

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, nullable=False)
    canBeRented = db.Column(db.Boolean, nullable=False)
    transportType = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    identifier = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    minutePrice = db.Column(db.Float)
    dayPrice = db.Column(db.Float)

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transportId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    timeStart = db.Column(db.DateTime, nullable=False)
    timeEnd = db.Column(db.DateTime)
    priceOfUnit = db.Column(db.Float, nullable=False)
    priceType = db.Column(db.String(20), nullable=False)
    finalPrice = db.Column(db.Float)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


# Пример функции для создания таблиц в базе данных
def create_tables():
    db.create_all()

# Пример функции для удаления всех таблиц из базы данных
def drop_tables():
    db.drop_all()
