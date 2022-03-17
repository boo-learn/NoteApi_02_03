from api import abort
from flask_babel import _


def get_or_404(model, id):
    obj = model.query.get(id)
    if not obj:
        abort(404, error=_("note %(id)s not found", id=id))
    return obj
