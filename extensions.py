from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

"""Create instances of the Flask extensions in the global scope"""

db = SQLAlchemy()
migrate = Migrate()
