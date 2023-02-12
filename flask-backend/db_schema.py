from sqlalchemy import Boolean, Column, create_engine, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import hashlib
import secrets
from fetch_card import Card
from pathlib import Path
from os import environ

# create the database interface
Base = declarative_base()

# a model of a user for the database
class User(Base):
    __tablename__='users'
    __table_args__ = {'extend_existing': True}

    userID = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable = False)
    passwordHash = Column(String(64), nullable = False)
    passwordSalt = Column(String(32), nullable = False)
    email = Column(String(30), nullable = False)

    # creating columns
    def __init__(self, username, passwordHash, passwordSalt, email):  
        self.username=username
        self.passwordHash=passwordHash
        self.passwordSalt=passwordSalt
        self.email=email


class Flashcard(Base):
    __tablename__='flashcards'
    __table_args__ = {'extend_existing': True}

    flashcardID = Column(Integer, primary_key=True)
    languageCode = Column(String(2), nullable = False)
    englishContent = Column(String(1000), nullable=False)
    languageContent = Column(String(1000), nullable=False)
    exampleUse = Column(String(1000))
    phoneticText = Column(String(1000))
    phoneticAudioLink = Column(String(40))
    isUserCreated = Column(Boolean)
    imageLink = Column(String(50))

    def __init__(self, languageCode, languageContent, isUserCreated=False, phoneticText=None, exampleUse=None):
        cardCreate = Card(languageContent, languageCode, "en")
        self.languageCode = languageCode
        self.englishContent = cardCreate.target
        self.languageContent = languageContent
        self.exampleUse = exampleUse
        self.phoneticText = phoneticText
        self.phoneticAudioLink = cardCreate.pronounciation
        self.isUserCreated = isUserCreated
        self.imageLink = cardCreate.image_url
    


# a model of a list item for the database
# it refers to a list
class UserCards(Base):
    __tablename__='user_cards'
    __table_args__ = {'extend_existing': True}

    userCardID = Column(Integer, primary_key=True)

    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    user = relationship(User)

    flashcardID = Column(Integer, ForeignKey('flashcards.flashcardID'), nullable=False)
    flashcard = relationship(Flashcard)

    comment = Column(String(200))
    correctAnswers = Column(Integer, nullable=False)
    totalEncountered = Column(Integer, nullable=False)
    isFavourite = Column(Boolean, nullable=False)
    lastEncountered = Column(DateTime)

    def __init__(self, userID, flashcardID, comment='', correctAnswers=0, totalEncountered=0, isFavourite=False, lastEncountered=None):
        self.userID = userID
        self.flashcardID = flashcardID
        self.comment = comment
        self.correctAnswers = correctAnswers
        self.totalEncountered = totalEncountered
        self.isFavourite = isFavourite
        self.lastEncountered = lastEncountered

class Course(Base):
    __tablename__='courses'
    __table_args__ = {'extend_existing': True}

    courseID = Column(Integer, primary_key=True)

    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    user = relationship(User)

    languageCode = Column(String(2), nullable = False)

    def __init__(self, userID, languageCode):
        self.userID = userID
        self.languageCode = languageCode


# put some data into the tables
def dbinit(path):
    engine = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()

    user_list = [
        User("Felicia", hashlib.sha256("Felicia".encode()).hexdigest(), secrets.token_hex(16), "felicia@gmail.com"),
        User("Petra", hashlib.sha256("Petra".encode()).hexdigest(), secrets.token_hex(16), "petra@gmail.com"),
        User("Johannes", hashlib.sha256("Johannes".encode()).hexdigest(), secrets.token_hex(16), "johannes@gmail.com"),
        User("Bob", hashlib.sha256("Bob".encode()).hexdigest(), secrets.token_hex(16), "Bob@gmail.com"),
        User("Jo", hashlib.sha256("Jo".encode()).hexdigest(), secrets.token_hex(16), "Jo@gmail.com"),
        User("Artemiy", hashlib.sha256("Artemiy".encode()).hexdigest(), secrets.token_hex(16), "Artemiy@gmail.com"),
        User("Yahia", hashlib.sha256("Yahia".encode()).hexdigest(), secrets.token_hex(16), "Yahia@gmail.com"),
        User("Oliver", hashlib.sha256("Oliver".encode()).hexdigest(), secrets.token_hex(16), "Oliver@gmail.com"),
        User("Raees", hashlib.sha256("Raees".encode()).hexdigest(), secrets.token_hex(16), "Raees@gmail.com")
        ]

    card_list = [
        Flashcard("es", "hola"),
        Flashcard("es", "cómo", True, "komo", "¿Cómo estás?"),
        Flashcard("es", "buenos", True, None, "Buenos días"),
        Flashcard("es", "mala", False)
    ]

    user_card_list = [
        UserCards(1, 2, "i cheated to find this one tbh"),
        UserCards(1, 3, "Good"),
        UserCards(1, 4, "literally never seen this in my life"),
        UserCards(2, 1, "this was easy"),
        UserCards(2, 2)
    ]

    course_list = [
        Course(1, "es"),
        Course(2, "es")
    ]

    try:
        session.add_all(user_list)
        session.add_all(card_list)
        session.add_all(user_card_list)
        session.add_all(course_list)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    path = Path(environ["VIRTUAL_ENV"]).parent / "flask-backend/database.db"
    if not path.is_file():
        dbinit(path)
    else:
        print("Database already exists.")
