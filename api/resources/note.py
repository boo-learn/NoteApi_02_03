from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import NoteSchema, NoteRequestSchema
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from webargs import fields
from api.models.tag import TagModel


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
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
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

    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        raise NotImplemented("Метод не реализован")
        return note_dict, 200


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