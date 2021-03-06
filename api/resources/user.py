from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(description="Получить пользователя по id")
    @doc(summary="Get User by id")
    @marshal_with(UserSchema, code=200)
    @doc(responses={"404": {"description": "User not found"}})
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        # if user is None:
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required(role="admin")
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Edit User")
    @marshal_with(UserSchema, code=200)
    @use_kwargs({"username": fields.Str(required=True)})
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @auth.login_required
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    # 1. Request Body (json, xml, string, ...) location=('json')
    # 2. Query param (localhost:PORT/ulr_source?name=Ivan&age=24 location=('query')
    # 3. Path (localhost:PORT/url/<param>)

    @doc(summary="Create new User")
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location=('json'))
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201
