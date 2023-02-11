from flask import Flask
app = Flask(__name__)

@app.route("/data")
def hello():
  return {
    "test": "test"
  }

if __name__ == "__main__":
  app.run()
