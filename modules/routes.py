from flask import Flask, json
from modules import app


@app.route('/health', methods = ['GET'])
def healthcheck():
    """
        Application healthcheck endpoints.
        Input: None
        Output: JSON
    """
    response = app.response_class(
        response = json.dumps({"status" : "UP"}),
        status = 200,
        mimetype = 'application/json'
    )
    return response


# Routing the tweeter users endpoints
from modules.users.views import users_routes

app.register_blueprint(users_routes)