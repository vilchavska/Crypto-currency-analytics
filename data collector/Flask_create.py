from flask import Flask
from functools import partial
import json
from flask_sqlalchemy import SQLAlchemy
from db_config import DATABASE_URL

# Initialize Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with custom JSON serialization
db = SQLAlchemy(
    app,
    engine_options={"json_serializer": partial(json.dumps, ensure_ascii=False)}
)