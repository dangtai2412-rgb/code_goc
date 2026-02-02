from flask import jsonify, g
from datetime import datetime
import uuid

def generate_request_id():
    if hasattr(g, "request_id"):
        return g.request_id
    g.request_id = str(uuid.uuid4())
    return g.request_id


def base_response(
    success,
    message,
    data=None,
    errors=None,
    meta=None,
    status_code=200
):
    body = {
        "success": success,
        "message": message,
        "status": status_code,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": generate_request_id()
    }

    if data is not None:
        body["data"] = data

    if errors is not None:
        body["errors"] = errors

    if meta is not None:
        body["meta"] = meta

    return jsonify(body), status_code


def success_response(data=None, message="Success", status_code=200, meta=None):
    return base_response(
        True,
        message,
        data=data,
        meta=meta,
        status_code=status_code
    )


def created_response(data=None, message="Created"):
    return base_response(
        True,
        message,
        data=data,
        status_code=201
    )


def error_response(message="An error occurred", status_code=400, errors=None):
    return base_response(
        False,
        message,
        errors=errors,
        status_code=status_code
    )


def not_found_response(message="Resource not found"):
    return base_response(
        False,
        message,
        status_code=404
    )


def validation_error_response(errors, message="Validation failed"):
    return base_response(
        False,
        message,
        errors=errors,
        status_code=422
    )


def unauthorized_response(message="Unauthorized"):
    return base_response(
        False,
        message,
        status_code=401
    )


def forbidden_response(message="Forbidden"):
    return base_response(
        False,
        message,
        status_code=403
    )


def server_error_response(message="Internal server error"):
    return base_response(
        False,
        message,
        status_code=500
    )