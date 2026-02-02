from flask import request
from api.responses import (
    success_response,
    error_response,
    validation_error_response
)


def get_request_data():
    if not request.is_json:
        return None, error_response("Request must be JSON", 415)

    data = request.get_json(silent=True)

    if data is None:
        return None, error_response("Invalid JSON body", 400)

    return data, None


def validate_request_schema(schema):
    data, error = get_request_data()

    if error:
        return None, error

    errors = schema.validate(data)

    if errors:
        return None, validation_error_response(errors)

    return data, None


def handle_get_request(service_func, *args, **kwargs):
    try:
        result = service_func(*args, **kwargs)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)


def handle_post_request(service_func, schema, *args, **kwargs):
    data, error = validate_request_schema(schema)

    if error:
        return error

    try:
        result = service_func(data, *args, **kwargs)
        return success_response(result, status_code=201)
    except Exception as e:
        return error_response(str(e), 500)


def handle_put_request(service_func, schema, *args, **kwargs):
    data, error = validate_request_schema(schema)

    if error:
        return error

    try:
        result = service_func(data, *args, **kwargs)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)


def handle_delete_request(service_func, *args, **kwargs):
    try:
        result = service_func(*args, **kwargs)
        return success_response(result, message="Deleted successfully")
    except Exception as e:
        return error_response(str(e), 500)