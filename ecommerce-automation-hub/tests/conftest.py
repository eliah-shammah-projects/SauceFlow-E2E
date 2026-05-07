import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def credentials():
    return {
        "user": os.getenv("SAUCE_USERNAME"),
        "password": os.getenv("SAUCE_PASSWORD"),
    }


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:5002"
