from quart import Blueprint
from src.utils.logger import setup_logger
import pkgutil
import importlib
import os
logger = setup_logger(__name__)
api_bp = Blueprint("scrapers", __name__, url_prefix="/api")

# Dynamically import all modules in this package
package_path = os.path.dirname(__file__)
for _, module_name, _ in pkgutil.iter_modules([package_path]):
    logger.info(f"{__name__}.{module_name}")
    importlib.import_module(f"{__name__}.{module_name}")