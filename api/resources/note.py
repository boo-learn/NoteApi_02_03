from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import NoteSchema, NoteRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from webargs import fields
from api.models.tag import TagModel
from helpers import shortcuts


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    @marshal_with(NoteSchema)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = shortcuts.get_or_404(NoteModel, note_id)
        return note, 200

    @auth.login_required
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        note.private = note_data.get("private") or note.private

        note.save()
        return note_schema.dump(note), 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required # 401
    @doc(responses={"204": {"description": "Ok"}})
    @doc(responses={"401": {"description": "Unauthorized"}})
    @doc(responses={"403": {"description": "Forbidden"}})
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        author = g.user
        note = shortcuts.get_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403)
        note.delete()
        return "", 204


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @marshal_with(NoteSchema(many=True))
    def get(self):
        notes = NoteModel.query.all()
        return notes, 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteRequestSchema, location="json")
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


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


# GET: /notes/filter?tags=[tag-1, tag-2, ...]
@doc(tags=['Notes'])
class NotesFilterResource(MethodResource):
    @doc(summary="Get notes by filter")
    @use_kwargs({"tags": fields.List(fields.Int())}, location="query")
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self, **kwargs):
        notes = NoteModel.query.join(NoteModel.tags).filter(TagModel.id.in_(kwargs["tags"])).all()
        return notes
