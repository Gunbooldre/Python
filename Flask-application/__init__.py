from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] ='mfssfjhsjdfhsjfhsjdfk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = LoginManager(app)


from application import main,database
db.create_all()