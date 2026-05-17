# third party
import requests

# project
from src.config.settings import URL
from src.logger import logger


response = requests.get(URL, verify=False)


logger.info(response.json())
