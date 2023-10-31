from flask import Blueprint, request
from flask_restful import Resource, Api
from models import Rent, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

admin_rent_blueprint = Blueprint('admin_rent', __name__)
admin_rent_api = Api(admin_rent_blueprint)

class AdminRentResource(Resource):
    @jwt_required
    def get(self, rentId=None):
        # Получение информации о аренде (по ID или всей аренде)
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        if rentId:
            rent = Rent.query.get(rentId)
            if not rent:
                return {"message": "Rent not found"}, 404

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

        start = request.args.get('start', default=0, type=int)
        count = request.args.get('count', default=10, type=int)

        rents = Rent.query.offset(start).limit(count).all()

        rent_list = []
        for rent in rents:
            rent_list.append({
                "id": rent.id,
                "transportId": rent.transportId,
                "userId": rent.userId,
                "timeStart": rent.timeStart.isoformat(),
                "timeEnd": rent.timeEnd.isoformat() if rent.timeEnd else None,
                "priceOfUnit": rent.priceOfUnit,
                "priceType": rent.priceType,
                "finalPrice": rent.finalPrice
            })

        return {"rents": rent_list}

    @jwt_required
    def post(self):
        # Создание новой аренды администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        transportId = data['transportId']
        userId = data['userId']
        timeStart = datetime.fromisoformat(data['timeStart'])
        timeEnd = datetime.fromisoformat(data['timeEnd']) if data.get('timeEnd') else None
        priceOfUnit = data['priceOfUnit']
        priceType = data['priceType']
        finalPrice = data.get('finalPrice', None)

        rent = Rent(
            transportId=transportId,
            userId=userId,
            timeStart=timeStart,
            timeEnd=timeEnd,
            priceOfUnit=priceOfUnit,
            priceType=priceType,
            finalPrice=finalPrice
        )
        db.session.add(rent)
        db.session.commit()

        return {"message": "Rent created successfully"}

    @jwt_required
    def put(self, rentId):
        # Изменение информации об аренде администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        data = request.get_json()
        transportId = data['transportId']
        userId = data['userId']
        timeStart = datetime.fromisoformat(data['timeStart'])
        timeEnd = datetime.fromisoformat(data['timeEnd']) if data.get('timeEnd') else None
        priceOfUnit = data['priceOfUnit']
        priceType = data['priceType']
        finalPrice = data.get('finalPrice', None)

        rent = Rent.query.get(rentId)
        if not rent:
            return {"message": "Rent not found"}, 404

        rent.transportId = transportId
        rent.userId = userId
        rent.timeStart = timeStart
        rent.timeEnd = timeEnd
        rent.priceOfUnit = priceOfUnit
        rent.priceType = priceType
        rent.finalPrice = finalPrice

        db.session.commit()

        return {"message": "Rent updated successfully"}

    @jwt_required
    def delete(self, rentId):
        # Удаление информации об аренде администратором
        current_user = get_jwt_identity()
        if not current_user['isAdmin']:
            return {"message": "Access denied"}, 403

        rent = Rent.query.get(rentId)
        if not rent:
            return {"message": "Rent not found"}, 404

        db.session.delete(rent)
        db.session.commit()

        return {"message": "Rent deleted successfully"}

admin_rent_api.add_resource(AdminRentResource, '/api/Admin/Rent', '/api/Admin/Rent/<int:rentId>')
