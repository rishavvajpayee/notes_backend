import gunicorn
import os
from os.path import join, dirname
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

gunicorn.SERVER_SOFTWARE = "Application Server"

bind = "0.0.0.0:" + os.getenv("PORT", "8085")
timeout = 60
workers = int(os.getenv("WORKER", 5))
threads = int(os.getenv("THREAD", 3))
worker_class = "gevent"
del gunicorn
