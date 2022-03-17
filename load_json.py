from config import BASE_DIR
from api.schemas.user import UserRequestSchema
from api.models.user import UserModel
from api import db

path_to_fixture = BASE_DIR / 'fixtures' / 'users.json'
# json --> dict --> object(Model)
with open(path_to_fixture, "r", encoding="UTF-8") as f:
    users_data = UserRequestSchema(many=True).loads(f.read())
    for user_data in users_data:
        user = UserModel(**user_data)
        db.session.add(user)
    db.session.commit()
print(f"{len(users_data)} users created")
