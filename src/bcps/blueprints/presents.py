from flask import Blueprint, jsonify
from bcps import server

bp = Blueprint("presents", __name__)


@bp.route("/api/v4/presents")
def presents():
    payload = {
        "presents": [
            {
                "title": "\nCat food +1000",
                "items": [
                    {
                        "itemId": 22,
                        "itemCategory": 0,
                        "amount": 100,
                        "title": "Cat food",
                    }
                ],
            },
        ]
    }
    data, headers = server.get_payload_response(payload)
    return jsonify(data), 200, headers


@bp.route("/api/v4/presents/count")
def presents_count():
    payload = {
        "count": 1,
    }
    data, headers = server.get_payload_response(payload)
    return jsonify(data), 200, headers


@bp.route("/api/v3/presents/reception")
def presents_accept():
    data, headers = server.get_payload_response()
    return jsonify(data), 200, headers
