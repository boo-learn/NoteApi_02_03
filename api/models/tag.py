from api import db
from api.models.class_additional import ModelMixin


class TagModel(db.Model, ModelMixin):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)