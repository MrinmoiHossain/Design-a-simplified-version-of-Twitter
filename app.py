import os
from modules import app

HOST = str(os.environ.get('HOST'))
PORT = str(os.environ.get('PORT'))

if __name__ == '__main__':
    app.run(host = HOST, port= PORT, debug = True)
