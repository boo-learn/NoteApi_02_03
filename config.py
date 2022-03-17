import os
from pathlib import Path

# base_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(__file__).parent


class Config:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'base.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR / "base.db"}'
    TEST_DATABASE_URI = f'sqlite:///{BASE_DIR / "test.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    LANGUAGES = ['en', 'ru']
