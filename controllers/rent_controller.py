from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Rent, Transport, db
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime

rent_blueprint = Blueprint('rent', __name__)
rent_api = Api(rent_blueprint)

class RentResource(Resource):
    @jwt_required
    def get(self, rentId):
        # Получение информации об аренде по ID
        rent = Rent.query.get(rentId)
        if not rent:
            return {"message": "Rent not found"}, 404

        # Проверка, является ли текущий пользователь арендатором или владельцем транспорта
        if rent.userId != current_user.id and rent.transport.ownerId != current_user.id:
            return {"message": "Access denied"}, 403

        # Преобразование информации об аренде в JSON и возврат
        return {
            "id": rent.id,
            "transportId": rent.transportId,
            "userId": rent.userId,
            "timeStart": rent.timeStart.isoformat(),
            "timeEnd": rent.timeEnd.isoformat() if rent.timeEnd else None,
            "priceOfUnit": rent.priceOfUnit,
            "priceType": rent.priceType,
            "finalPrice": rent.finalPrice
        }

    @jwt_required
    def post(self, transportId):
        # Аренда транспорта
        transport = Transport.query.get(transportId)
        if not transport:
            return {"message": "Transport not found"}, 404

        if transport.ownerId == current_user.id:
            return {"message": "You cannot rent your own transport"}, 400

        data = request.get_json()
        rentType = data.get('rentType', 'Minutes')

        if rentType not in ['Minutes', 'Days']:
            return {"message": "Invalid rentType"}, 400

        # Создание записи об аренде
        current_time = datetime.now()
        rent = Rent(
            transportId=transport.id,
            userId=current_user.id,
            timeStart=current_time,
            priceOfUnit=transport.minutePrice if rentType == 'Minutes' else transport.dayPrice,
            priceType=rentType,
            finalPrice=0.0
        )

        db.session.add(rent)
        db.session.commit()

        return {"message": "Rent created successfully"}

class RentEndResource(Resource):
    @jwt_required
    def post(self, rentId):
        # Завершение аренды транспорта
        rent = Rent.query.get(rentId)
        if not rent:
            return {"message": "Rent not found"}, 404

        if rent.userId != current_user.id:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        rent.timeEnd = datetime.now()
        db.session.commit()

        # Вычисление и установка finalPrice в зависимости от времени аренды
        if rent.priceType == 'Minutes':
            minutes = (rent.timeEnd - rent.timeStart).total_seconds() / 60
            rent.finalPrice = minutes * rent.priceOfUnit
        else:
            days = (rent.timeEnd - rent.timeStart).days
            rent.finalPrice = days * rent.priceOfUnit

        db.session.commit()
        return {"message": "Rent ended successfully"}

class RentListResource(Resource):
    @jwt_required
    def get(self):
        # Получение истории аренд текущего пользователя
        rents = Rent.query.filter_by(userId=current_user.id).all()
        rent_history = []

        for rent in rents:
            rent_history.append({
                "id": rent.id,
                "transportId": rent.transportId,
                "timeStart": rent.timeStart.isoformat(),
                "timeEnd": rent.timeEnd.isoformat() if rent.timeEnd else None,
                "priceOfUnit": rent.priceOfUnit,
                "priceType": rent.priceType,
                "finalPrice": rent.finalPrice
            })

        return {"rent_history": rent_history}

rent_api.add_resource(RentResource, '/api/Rent/<int:rentId>')
rent_api.add_resource(RentEndResource, '/api/Rent/End/<int:rentId>')
rent_api.add_resource(RentListResource, '/api/Rent/MyHistory')
