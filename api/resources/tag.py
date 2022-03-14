from webargs import fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with, use_kwargs
from api.models.note import NoteModel
from api.schemas.note import NoteSchema
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema
from api import abort


# /tags/<id> <-- GET PUT DELETE
@doc(tags=["Tags"])
class TagResource(MethodResource):
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200


@doc(tags=["Tags"])
class TagsListResource(MethodResource):
    @use_kwargs(TagRequestSchema, location=('json'))
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if tag.id is None:
            abort(400, error=f"Tag with name={tag.name} already exists")
        return tag, 201

