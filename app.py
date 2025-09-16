from flask import Flask, jsonify
import socket
import os
import logging


def create_app():
    app = Flask(__name__)

    # Logging setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    logger = logging.getLogger("app")

    @app.route("/")
    def hello():
        try:
            ip = socket.gethostbyname(socket.gethostname())
            return ip
        except Exception:
            logger.exception("Failed to resolve host IP")
            return "Internal Server Error", 500

    @app.route("/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.route("/version")
    def version():
        return jsonify(version=os.environ.get("APP_VERSION", "0.0.0"))

    @app.route("/whoami")
    def whoami():
        try:
            return jsonify(
                hostname=socket.gethostname(),
                ip=socket.gethostbyname(socket.gethostname())
            )
        except Exception:
            return jsonify(error="unresolvable"), 500

    # added test route to verify
    @app.route("/evatest")
    def evatest():
        return jsonify(test="ok")

    @app.errorhandler(500)
    def handle_500(_):
        return "Internal Server Error", 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", "80"))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=port, host="0.0.0.0")
