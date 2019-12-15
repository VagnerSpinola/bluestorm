import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuracoes da applicacao
# ===================================================================================
DB_NAME = 'bluestorm.db'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AJASIQQ#^fh@#d&(khs!@2_{;[].</JS;:SC/AS5P0S2GA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_NAME) 
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)