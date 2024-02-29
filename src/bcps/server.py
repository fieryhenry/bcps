from typing import Any, Optional
import flask
import time

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


def get_payload_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Nyanko-Signature": "A",
    }


def get_timestamp() -> int:
    return int(time.time())


def get_payload_response(
    payload: Optional[dict[str, Any]] = None, status_code: int = 1
) -> tuple[dict[str, Any], dict[str, str]]:
    nonce = flask.request.args.get("nonce")
    data: dict[str, Any] = {
        "statusCode": status_code,
        "nonce": nonce,
        "timestamp": get_timestamp(),
    }
    if payload is not None:
        data["payload"] = payload
    headers = get_payload_headers()
    return data, headers


def register_blueprints():
    from bcps.blueprints import __blueprints__

    for blueprint in __blueprints__:
        add_blueprint(blueprint)


def start(host: str, port: int):
    register_blueprints()
    app.run(host=host, port=port)


def add_blueprint(bp: flask.Blueprint):
    app.register_blueprint(bp)


if __name__ == "__main__":
    start("0.0.0.0", 5000)
