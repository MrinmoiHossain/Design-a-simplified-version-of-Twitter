import os
from modules import app

# Set application host & port from the environment variable
HOST = str(os.environ.get('HOST'))
PORT = str(os.environ.get('PORT'))

# Application main starting method
if __name__ == '__main__':
    app.run(host = HOST, port= PORT, debug = True)
