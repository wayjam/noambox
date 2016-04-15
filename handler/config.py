import os.path
import logging
import model
from api import json_utils


DATA_PATH = './data/'
LOG_FILE = 'noambox.log'
CONFIG_FILE = 'config.json'
HISTORY_FILE = 'history.json'

# log basic config
logging.basicConfig(
    format="%(asctime)s - [%(process)d]%(filename)s:%(lineno)d - %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%I:%S',
    filename=os.path.expanduser(DATA_PATH + LOG_FILE),
    level=logging.INFO
)
# Set up our own logger
logger = logging.getLogger('noambox')
logger.setLevel(logging.INFO)
logger.info("*****Noambox started*****")


class Config:

    def __init__(self):
        self.load()

    def load(self):
        if not(os.path.exists(DATA_PATH)):
            os.makedirs(DATA_PATH)

        self.config = model.Config()
        if not(os.path.isfile(DATA_PATH + CONFIG_FILE)):
            os.mknod(DATA_PATH + CONFIG_FILE)
            self.save('config')
        else:
            with open(DATA_PATH + CONFIG_FILE, 'r') as f:
                json_utils.json2obj(f, self.config)

        self.history = model.History()
        if not(os.path.isfile(DATA_PATH + HISTORY_FILE)):
            os.mknod(DATA_PATH + HISTORY_FILE)
            self.save('history')
        else:
            with open(DATA_PATH + HISTORY_FILE, 'r') as f:
                json_utils.json2obj(f, self.history)

    def save(self,t = None):
        if t != 'config':
            with open(DATA_PATH + HISTORY_FILE, 'w') as f:
                json_utils.obj2jsons(f, self.history)
        if t != 'history':
            with open(DATA_PATH + CONFIG_FILE, 'w') as f:
                json_utils.obj2jsons(f, self.config)


# Initialize  when it starts
data = Config()
