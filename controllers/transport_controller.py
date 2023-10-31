from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Transport, db
from flask_jwt_extended import jwt_required

transport_blueprint = Blueprint('transport', __name__)
transport_api = Api(transport_blueprint)

class TransportResource(Resource):
    @jwt_required
    def get(self, id):
        # Получение информации о транспорте по id
        transport = Transport.query.get(id)
        if not transport:
            return {"message": "Transport not found"}, 404

        # Преобразование информации о транспорте в JSON и возврат
        return {
            "id": transport.id,
            "ownerId": transport.ownerId,
            "canBeRented": transport.canBeRented,
            "transportType": transport.transportType,
            "model": transport.model,
            "color": transport.color,
            "identifier": transport.identifier,
            "description": transport.description,
            "latitude": transport.latitude,
            "longitude": transport.longitude,
            "minutePrice": transport.minutePrice,
            "dayPrice": transport.dayPrice
        }

    @jwt_required
    def put(self, id):
        # Изменение информации о транспорте по id
        transport = Transport.query.get(id)
        if not transport:
            return {"message": "Transport not found"}, 404

        # Проверка, является ли текущий пользователь владельцем этого транспорта
        if transport.ownerId != current_user_id():
            return {"message": "You are not the owner of this transport"}, 403

        # Обновление информации о транспорте на основе параметров запроса
        data = request.get_json()
        transport.canBeRented = data['canBeRented']
        transport.model = data['model']
        transport.color = data['color']
        transport.identifier = data['identifier']
        transport.description = data.get('description')
        transport.latitude = data['latitude']
        transport.longitude = data['longitude']
        transport.minutePrice = data.get('minutePrice')
        transport.dayPrice = data.get('dayPrice')

        db.session.commit()
        return {"message": "Transport updated successfully"}

    @jwt_required
    def delete(self, id):
        # Удаление транспорта по id
        transport = Transport.query.get(id)
        if not transport:
            return {"message": "Transport not found"}, 404

        # Проверка, является ли текущий пользователь владельцем этого транспорта
        if transport.ownerId != current_user_id():
            return {"message": "You are not the owner of this transport"}, 403

        db.session.delete(transport)
        db.session.commit()
        return {"message": "Transport deleted successfully"}

class TransportListResource(Resource):
    @jwt_required
    def post(self):
        # Добавление нового транспорта
        data = request.get_json()
        transport = Transport(
            ownerId=current_user_id(),
            canBeRented=data['canBeRented'],
            transportType=data['transportType'],
            model=data['model'],
            color=data['color'],
            identifier=data['identifier'],
            description=data.get('description'),
            latitude=data['latitude'],
            longitude=data['longitude'],
            minutePrice=data.get('minutePrice'),
            dayPrice=data.get('dayPrice')
        )

        db.session.add(transport)
        db.session.commit()
        return {"message": "Transport added successfully"}

def current_user_id():
    return get_jwt_identity()

transport_api.add_resource(TransportResource, '/api/Transport/<int:id>')
transport_api.add_resource(TransportListResource, '/api/Transport')
