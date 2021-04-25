from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True

db = SQLAlchemy(app)
api = Api(app)
api.prefix = '/api'

#Model
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    birthday = db.Column(db.String(20))

    def __repr__(self):
        return 'Id: {}, first_name: {}'.format(self.id, self.first_name) 

#Resource
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'birthday': fields.String,
}

user_list_fields = {
    'users': fields.List(fields.Nested(user_fields)),
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('first_name', type=str, required=True, location=['json'],
                              help='first_name parameter is required')
user_post_parser.add_argument('last_name', type=str, required=True, location=['json'],
                              help='last name parameter is required')
user_post_parser.add_argument('birthday', type=str, required=True, location=['json'],
                              help='birthday parameter is required')


class UsersResource(Resource):
    def get(self, user_id=None,first_name=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return marshal(user, user_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)


            user = User.query.filter_by(**args).order_by(User.id)
            if limit:
                user = user.limit(limit)

            if offset:
                user = user.offset(offset)

            user = user.all()

            return marshal({
                'count': len(user),
                'users': [marshal(u, user_fields) for u in user]
            }, user_list_fields)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()

        user = User(**args)
        db.session.add(user)
        db.session.commit()

        return user

    @marshal_with(user_fields)
    def put(self, user_id=None):
        user = User.query.get(user_id)

        if 'first_name' in request.json:
            user.name = request.json['first_name']

        if 'last_name' in request.json:
            user.name = request.json['last_name']
            
        if 'birthday' in request.json:
            user.name = request.json['birthday']

        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, user_id=None):
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        return user


api.add_resource(UsersResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run()
