from flask import Flask, json
from modules import app


@app.route('/health', methods = ['GET'])
def healthcheck():
    response = app.response_class(
        response = json.dumps({"status" : "UP"}),
        status = 200,
        mimetype = 'application/json'
    )
    return response


from modules.users.views import users_routes

app.register_blueprint(users_routes)