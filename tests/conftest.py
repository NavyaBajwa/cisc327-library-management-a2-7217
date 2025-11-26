import pytest
from database import init_database, reset_database, add_sample_data

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_database()
    reset_database()
    add_sample_data()