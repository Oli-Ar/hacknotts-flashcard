from db_schema import Flashcard, User, UserCards, Course

from flask import Flask, request, jsonify
from flask_login import current_user, logout_user

from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy import create_engine

from os import environ
from pathlib import Path
import hashlib
import datetime

import jwt

app = Flask(__name__)
path = Path(environ["VIRTUAL_ENV"]).parent / "flask-backend/database.db"
engine = create_engine(f"sqlite:///{path}")
Session = sessionmaker(engine)
session = Session()

@app.route("/data")
def data():
  # Helper function to handle request arguments
  def handle_lang(lang):
    # Get all flashcard IDs for a given language, map to get first (only) element of tuple
    lang_ids = list(map(lambda x: x[0], session.query(Flashcard.flashcardID).filter_by(languageCode=lang).all()))
    return lang_ids

  def handle_id(id):
    # Fetch flashcard with given ID
    card = session.query(Flashcard).filter_by(flashcardID=id).first()
    # Get list of column names for the Flashcard class
    columns = [c.key for c in class_mapper(card.__class__).columns]
    # Parse the returned object into a dictionary so flask can serialize it
    return dict((c, getattr(card, c)) for c in columns)

  actions = {'lang': handle_lang, 'id': handle_id}
  for (key, value) in request.args.items():
    if key in actions:
      return actions[key](value)




secretKey = 'FgG_mB7PEEqceDtl8O-Zdw'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    inputUsername = data.get('user')
    inputPassword = data.get('pwd')

    if not inputUsername or not inputPassword:
        return 'Username and password are required', 400

    # Add your logic for checking the username and password here
    associatedPass = session.query(User).filter_by(username=inputUsername).first()

    if associatedPass is None:
        return 'Username or password is incorrect', 401
    
    passSalt = associatedPass.passwordSalt
    passHash = associatedPass.passwordHash

    if hashlib.sha256((inputPassword+passSalt).encode()).hexdigest() != passHash:
        return 'Username or password is incorrect', 401

    # If the username and password are correct, generate a JWT token
    # Generate a JSON Web Token (JWT) for the user
    payload = {
        'sub': inputUsername,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secretKey, algorithm='HS256')


    return jsonify({'token': token.decode('utf-8')})




if __name__ == "__main__":
  app.run()