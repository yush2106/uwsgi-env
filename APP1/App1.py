from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from werkzeug.middleware.dispatcher import DispatcherMiddleware

flask_app = Flask(__name__)  #Flask app
CORS(flask_app)  #add CORS
#app.config['DEBUG'] = True  #debug mode

ProjectName = ""
#ProjectName = "/MyWebAPI"

@flask_app.route(ProjectName + "/", methods=['GET'])
def Hello():
  return '<h1>Hello, App1</h1>'  #hello response
#App location
app = DispatcherMiddleware(None, {
  "/App1": flask_app
})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
  #serve(app, host="0.0.0.0", port=5000, threads=5)  #run waitress server