import requests
from loguru import logger

r = requests.get("http://localhost:8899/user/")
logger.info(r.status_code)
logger.info(r.text)