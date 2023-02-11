from flask import Flask
from flask_login import login_user, current_user, logout_user, login_required
app = Flask(__name__)

@app.route("/data")
def hello():
  return {
    "test" : "test"
  }


#TODO we could use the flask_login module to track user session, and ensure some pages are only accessible if user has logged in.

#this will be the landing page of the website, we can have information about the web app and links to login and registration
@app.route("/")
def index():
  pass


@app.route("/login",  methods=["GET", "POST"])
def login():
  #TODO create a login form, possibly using the forms module flask can provide. this route will be for the login
  #TODO authenticate user, and if autheticated then update the user session appropriately

  #if the user has been authenticated already (session is active)
  if current_user.is_authenticated:
    return redirect(url_for('home'))

  
  pass

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route("/register",  methods=["GET", "POST"])
def register():
  #TODO just like the login route. 
  pass

#this will be the home page for the user when they log in
@app.route("/home")
def home():
  #TODO get session information (user details, and the subjects they take), generate flash cards here
  pass

#function adds a specific card to favourites
@app.route("/add_favourite/<int:card_id>", methods=["GET", "POST"])
def add_favourite(post_id):
  #TODO add the card to database appropriately
  pass

#this page will show all the favourite cards of a certain user
@app.route("/favourites",  methods=["GET", "POST"])
def favourites():
  pass
  




if __name__ == "__main__":
  app.run()

