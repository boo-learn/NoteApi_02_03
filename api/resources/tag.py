from webargs import fields
from flask_apispec.views import MethodResource
from flask_apispec import doc, marshal_with, use_kwargs
from api.models.note import NoteModel
from api.schemas.note import NoteSchema
from api.models.tag import TagModel
from api.schemas.tag import TagSchema
from api import abort


# /tags/<id> <-- GET PUT DELETE
@doc(tags=["Tags"])
class TagSource(MethodResource):
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        return tag, 200


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        print("note kwargs = ", kwargs)
        ...
        ...
        return note, 200
