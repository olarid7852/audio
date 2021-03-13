import pytest
import tempfile
import os
from app.app import create_app, register_extensions
from app.db import db
from app.config.config import TestingConfig


@pytest.fixture
def client():
    db_fd, temp_file_name = tempfile.mkstemp()
    TestingConfig.SQLALCHEMY_DATABASE_URI = f'sqlite:///{temp_file_name}'
    app = create_app(TestingConfig)
    db.db.init_app(app)
    register_extensions(app)
    with app.test_client() as client:
        with app.app_context() as context:
            context.push()
            db.db.create_all()
        yield client