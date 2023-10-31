from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Transport, db
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_transport_blueprint = Blueprint('admin_transport', __name__)
admin_transport_api = Api(admin_transport_blueprint)

class AdminTransportResource(Resource):
    @jwt_required
    def get(self, id=None):
        # Получение информации о транспорте (всех транспортах или по ID)
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        if id:
            transport = Transport.query.get(id)
            if not transport:
                return {"message": "Transport not found"}, 404

            return {
                "id": transport.id,
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

        start = request.args.get('start', default=0, type=int)
        count = request.args.get('count', default=10, type=int)
        transport_type = request.args.get('transportType', default='All', type=str)

        if transport_type == 'All':
            transports = Transport.query.offset(start).limit(count).all()
        else:
            transports = Transport.query.filter_by(transportType=transport_type).offset(start).limit(count).all()

        transport_list = []
        for transport in transports:
            transport_list.append({
                "id": transport.id,
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
            })

        return {"transport": transport_list}

    @jwt_required
    def post(self):
        # Создание нового транспорта администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        canBeRented = data['canBeRented']
        transportType = data['transportType']
        model = data['model']
        color = data['color']
        identifier = data['identifier']
        description = data['description']
        latitude = data['latitude']
        longitude = data['longitude']
        minutePrice = data['minutePrice']
        dayPrice = data['dayPrice']

        transport = Transport(
            canBeRented=canBeRented,
            transportType=transportType,
            model=model,
            color=color,
            identifier=identifier,
            description=description,
            latitude=latitude,
            longitude=longitude,
            minutePrice=minutePrice,
            dayPrice=dayPrice
        )
        db.session.add(transport)
        db.session.commit()

        return {"message": "Transport created successfully"}

    @jwt_required
    def put(self, id):
        # Изменение информации о транспорте администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        canBeRented = data['canBeRented']
        model = data['model']
        color = data['color']
        identifier = data['identifier']
        description = data['description']
        latitude = data['latitude']
        longitude = data['longitude']
        minutePrice = data['minutePrice']
        dayPrice = data['dayPrice']

        transport = Transport.query.get(id)
        if not transport:
            return {"message": "Transport not found"}, 404

        transport.canBeRented = canBeRented
        transport.model = model
        transport.color = color
        transport.identifier = identifier
        transport.description = description
        transport.latitude = latitude
        transport.longitude = longitude
        transport.minutePrice = minutePrice
        transport.dayPrice = dayPrice

        db.session.commit()

        return {"message": "Transport updated successfully"}

    @jwt_required
    def delete(self, id):
        # Удаление информации о транспорте администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        transport = Transport.query.get(id)
        if not transport:
            return {"message": "Transport not found"}, 404

        db.session.delete(transport)
        db.session.commit()

        return {"message": "Transport deleted successfully"}

admin_transport_api.add_resource(AdminTransportResource, '/api/Admin/Transport', '/api/Admin/Transport/<int:id>')
