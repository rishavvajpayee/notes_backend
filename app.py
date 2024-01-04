from conf.database import Config
from gevent.pywsgi import WSGIServer
from factory import create_app
from flask_cors import CORS
from utils.authentication import before_check
from constants import common
from utils.responses import handle_response

app = create_app()
app.config["CORS_METHODS"] = Config.CORS_METHODS
app.config["CORS_ORIGINS"] = [Config.CORS_ORIGINS]
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI


@app.before_request
def before_request():
    return before_check()


@app.route("/", methods=["GET"])
def health_check():
    return handle_response(200, common["SUCCESS"], {"status": "Working"})


if __name__ == "__main__":
    """
    uncomment them when you want to debug
    app.debug=True
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
    """

    http_server = WSGIServer(("127.0.0.1", int(Config.PORT)), app)
    print(f"Server running locally on: http://127.0.0.1:{int(Config.PORT)}")
    http_server.serve_forever()
