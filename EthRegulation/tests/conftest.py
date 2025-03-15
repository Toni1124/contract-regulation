import pytest
from app import create_app
from app.extensions import db
from typing import Generator, Any

@pytest.fixture
def app() -> Generator[Any, Any, None]:
    app = create_app('app.config.TestConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app: Any) -> Any:
    return app.test_client()

@pytest.fixture
def runner(app: Any) -> Any:
    return app.test_cli_runner() 