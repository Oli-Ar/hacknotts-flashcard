from db_schema import Flashcard

from flask import Flask, request
from flask_login import current_user, logout_user

from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine("sqlite:///database.db")
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


if __name__ == "__main__":
  app.run()