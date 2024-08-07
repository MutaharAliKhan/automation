
import pytest
from database.database_connection import get_environment_config


@pytest.fixture(scope='session')
def base_url():
    data = get_environment_config(r"D:\MyRecentProjects\Data_Utility\database\env_config.json")
    return data.get("URL")
