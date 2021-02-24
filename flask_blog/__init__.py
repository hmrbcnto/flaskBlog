
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#Initialize app
app = Flask(__name__)

#Configuring app secret key
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Configuring .db file location. Triple forward slash means CWD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Creating an instance of our database
db = SQLAlchemy(app)

#Creating an instance of our encryptor
bcrypt = Bcrypt(app)

from flask_blog import routes
