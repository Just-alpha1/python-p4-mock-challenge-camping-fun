#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Campers(Resource):
    def get(self):
        campers = Camper.query.all()
        return [camper.to_dict() for camper in campers], 200

    def post(self):
        data = request.get_json()
        try:
            camper = Camper(**data)
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400


class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return {"error": "Camper not found"}, 404
        return camper.to_dict(rules=('signups', '-signups.camper', '-signups.activity.signups')), 200

    def patch(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return {"error": "Camper not found"}, 404
        data = request.get_json()
        try:
            for attr in data:
                setattr(camper, attr, data[attr])
            db.session.commit()
            return camper.to_dict(), 202
        except ValueError:
            return {"errors": ["validation errors"]}, 400


class Activities(Resource):
    def get(self):
        activities = Activity.query.all()
        return [activity.to_dict() for activity in activities], 200


class ActivityById(Resource):
    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            return {"error": "Activity not found"}, 404
        db.session.delete(activity)
        db.session.commit()
        return '', 204


class Signups(Resource):
    def post(self):
        data = request.get_json()
        try:
            signup = Signup(**data)
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400


api.add_resource(Campers, '/campers')
api.add_resource(CamperById, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(ActivityById, '/activities/<int:id>')
api.add_resource(Signups, '/signups')


@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
