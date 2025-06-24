import logging
from datetime import datetime


logger = logging.getLogger(__name__)
# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{datetime.now()}-etl_process.log"),
        logging.StreamHandler()
    ]
)
