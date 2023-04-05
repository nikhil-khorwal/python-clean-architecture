from app.application.app import create_app
app = create_app("testing")
import pytest

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield
