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

# PUT: /notes/<note_id>/tags
@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        # print("note kwargs = ", kwargs)
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            # TODO: добавить проверку существования тега
            note.tags.append(tag)
        note.save()
        return note, 200
