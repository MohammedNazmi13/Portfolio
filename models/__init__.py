from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import User, Project, Contact, SiteContent
