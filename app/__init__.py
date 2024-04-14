"""init"""

import logging
import time
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app import routes

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

if not os.path.exists("results"):
    os.makedirs("results")

webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

#dam acces la ingestor thread-urilor pentru functiile de calcul de rezultate
webserver.tasks_runner.ingestor = webserver.data_ingestor

webserver.job_counter = 1

webserver.json.sort_keys = False


#Logger-ul este creat, se seteaza formatul mesajelor, formatul orei
#si se activeaza RotatingFileHandler pentru a suprascrie fisierul cand atinge limita
webserver.logger = logging.getLogger(__name__)
logging.basicConfig(filename="server.log", level=logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s")
formatter.converter = time.gmtime
handler = RotatingFileHandler("server.log", maxBytes=100000, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
webserver.logger.addHandler(handler)
