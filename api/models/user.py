from api import db, Config, ma
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from api.models.class_additional import ModelMixin


class UserModel(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='dynamic')
    is_staff = db.Column(db.Boolean(), default=False, server_default="false", nullable=False)
    role = db.Column(db.String(32), nullable=False, server_default="simple_user", default="simple_user")

    def __init__(self, username, password, role="simple_user", is_staff=False):
        self.username = username
        self.role = role
        self.hash_password(password)

    def get_roles(self):
        return [self.role]

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
