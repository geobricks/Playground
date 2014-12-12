from geobricks_data_manager.core.data_manager_core import DataManager

# N.B. GHG DEMO
from geobricks_playground.config.config_ghg_demo import settings


def get_data_manager():
    return DataManager(settings)