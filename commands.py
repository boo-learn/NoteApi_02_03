from api import app
import click
import json
from config import BASE_DIR
from api.schemas.user import UserRequestSchema
from api.models.user import UserModel
from api.models.note import NoteModel
from api import db


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:") or "admin"
    password = input("Password[default 'admin']:") or "admin"
    user = UserModel(username, password, role="admin", is_staff=True)
    user.save()
    if user.id:
        print(f"Superuser create successful! id={user.id}")
    else:
        print("Пользователь с таким именем уже существует")


@app.cli.command('my-command')
@click.argument('param')
def my_command(param):
    """
    Demo command with param
    """
    print(f"Run my_command with param {param}")


@app.cli.command('fixture')
@click.argument('do')
def load_fixture(do):
    models = {
        "NoteModel": NoteModel,
        "UserModel": UserModel,
    }
    if do == "load":
        path_to_fixture = BASE_DIR / 'fixtures' / 'notes.json'
        with open(path_to_fixture, "r", encoding="UTF-8") as f:
            data = json.load(f)
            model = data["model"]
            class_model = models[model]
            for obj_data in data["records"]:
                obj_model = class_model(**obj_data)
                db.session.add(obj_model)
            db.session.commit()
        print(f"{len(data['records'])} objects created")
