from flask import Flask
from reactpy import component
from reactpy.backend.flask import configure

@component
def App():
   return

flask = Flask(__name__)
configure(flask, App)

if __name__ == "__main__":
    flask.run(debug=True, port=5000)

