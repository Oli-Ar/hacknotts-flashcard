from db_schema import Flashcard, User, UserCards, Course
from flask import Flask, request, jsonify
from flask_login import current_user, logout_user
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy import create_engine
from os import environ
from pathlib import Path
import hashlib
import secrets
import datetime
from authlib.jose import jwt
import time
  
app = Flask(__name__)
CORS(app)

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




jwk = {
  "crv": "P-256",
  "kty": "EC",
  "alg": "ES256",
  "use": "sig",
  "kid": "a32fdd4b146677719ab2372861bded89",
  "d": "5nYhggWQzfPFMkXb7cX2Qv-Kwpyxot1KFwUJeHsLG_o",
  "x": "-uTmTQCbfm2jcQjwEa4cO7cunz5xmWZWIlzHZODEbwk",
  "y": "MwetqNLq70yDUnw-QxirIYqrL-Bpyfh4Z0vWVs_hWCM"
}

header = {"alg": "ES256"}

@app.route('/Login', methods=['POST'])
def Login():
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
    "iss": "https://LocalHost:5000",
    "aud": "api1",
    "sub": inputUsername,
    "exp": int(time.time()) + 3600,
    "iat": int(time.time())
}
    token = jwt.encode(header, payload, jwk)
    response = jsonify({'token': token.decode('utf-8')})
    response.headers['Access-Control-Allow-Origin'] = '*' # This is a hack to allow CORS

    return response


@app.route('/Register', methods=['POST'])
def Register():
  print("balls")
  data = request.get_json()
  inputUsername = data.get('user')
  inputPassword = data.get('pwd')
  inputEmail = data.get('email')

  existingUser = session.query(User).filter_by(username=inputUsername).first()
  if existingUser is not None:
    return 'Username already exists', 400

  passSalt = secrets.token_hex(16)
  passHash = hashlib.sha256((inputPassword+passSalt).encode()).hexdigest()

  newUser = User(username=inputUsername, passwordHash=passHash, passwordSalt=passSalt, email=inputEmail)
  session.add(newUser)
  session.commit()
  return {"msg": "User created successfully"}, 200

  



  

  



if __name__ == "__main__":
  app.run()