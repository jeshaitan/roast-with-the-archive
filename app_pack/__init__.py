from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app_pack import routes
