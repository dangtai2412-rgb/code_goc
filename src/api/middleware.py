from flask import request, jsonify, g
import time



def log_request():
    print("\n========== REQUEST ==========")
    print(f"Method : {request.method}")
    print(f"URL    : {request.url}")

    # In headers
    print("Headers:")
    for k, v in request.headers.items():
        print(f"  {k}: {v}")

    # In body an toàn
    body = request.get_data(as_text=True)
    if body:
        print("Body :", body)
    else:
        print("Body : (empty)")

    print("=============================\n")




def start_timer():
    g.start_time = time.time()

def end_timer(response):
    duration = time.time() - g.start_time
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response




def handle_cors():
    response = jsonify({"status": "ok"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response, 200




def format_response(data=None, message="Success", status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status



def handle_error(error):
    code = getattr(error, "code", 500)

    return jsonify({
        "success": False,
        "message": "Server error",
        "error": str(error)
    }), code



def add_headers(response):
    response.headers["X-App"] = "Flask API"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response




def setup_middleware(app):

    # BEFORE REQUEST
    @app.before_request
    def before_request():

        # Start timer
        start_timer()

        # Log request
        log_request()

        # Handle OPTIONS for CORS
        if request.method == "OPTIONS":
            return handle_cors()


    # AFTER REQUEST
    @app.after_request
    def after_request(response):

        # Add headers
        response = add_headers(response)

        # End timer
        response = end_timer(response)

        return response


    # ERROR HANDLER
    @app.errorhandler(Exception)
    def global_error_handler(error):
        return handle_error(error)