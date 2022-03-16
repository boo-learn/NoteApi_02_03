from api import app
from api.models.user import UserModel
import click


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